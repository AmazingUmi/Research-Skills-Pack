import { test } from "node:test";
import assert from "node:assert/strict";
import { mkdtemp, readFile, rm } from "node:fs/promises";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { runInNewContext } from "node:vm";
import { main, parseArgs } from "../roles/literature/fulltext/scripts/batch_download.mjs";
import { chooseRoute, chooseDirectUrlRoute } from "../roles/literature/fulltext/scripts/lib/routing.mjs";
import { downloadCnkiDirectUrl } from "../roles/literature/fulltext/scripts/lib/cnki.mjs";

test("explicit URL and OA-only scope survive Chinese language routing", () => {
  const args = parseArgs(["node", "batch", "--title", "中文论文", "--open-access", "--si"]);
  assert.equal(args.route, "open_access");
  assert.equal(chooseRoute(args).provider, "open_access");
  assert.equal(chooseDirectUrlRoute({ ...args, pdfUrl: "https://repository.test/paper.pdf" }).provider, "direct_url");
  assert.equal(chooseDirectUrlRoute({ ...args, pdfUrl: "https://www.cnki.net/paper.pdf" }).provider, "direct_url");
  assert.equal(chooseRoute({title: "中文论文"}).provider, "cnki");
  assert.throws(() => parseArgs(["node", "batch", "--open-access", "--topic", "生态", "--no-si"]), /OA-only/);
});

test("a verification page leaves its tab open for the user", async (t) => {
  const url = "https://www.cnki.net/paper.pdf";
  const paths = [];
  t.mock.method(globalThis, "fetch", async (endpoint, options) => {
    const path = new URL(endpoint).pathname;
    paths.push(path);
    if (path === "/new") return Response.json({ targetId: "fixture" });
    if (path === "/info") return Response.json({ ready: "complete", url, title: "Human verification" });
    if (path === "/eval") {
      assert.match(options.body, /document.body.innerText/);
      return Response.json({ value: "Verify you are human" });
    }
    throw new Error("Unexpected interaction " + path);
  });
  const result = await downloadCnkiDirectUrl("https://proxy.test", url, "title", ".");
  assert.equal(result.status, "publisher_verification_waiting_user");
  assert.equal(result.tab, "fixture");
  assert.deepEqual(paths, ["/new", "/info", "/info", "/eval"]);
});

test("OA-only CLI uses public sources for Chinese title and honors a supplied PDF", async (t) => {
  const folder = await mkdtemp(join(tmpdir(), "fulltext-routes-"));
  t.after(() => rm(folder, { recursive: true, force: true }));
  t.mock.method(console, "log", () => {});
  const destinations = [];
  t.mock.method(globalThis, "fetch", async (endpoint) => {
    const { hostname } = new URL(endpoint);
    destinations.push(hostname);
    if (hostname === "repository.test") return new Response("%PDF-1.7 fixture", {headers: {"content-type": "application/pdf"}});
    if (hostname === "export.arxiv.org") return new Response("<feed/>");
    if (hostname === "api.crossref.org") return Response.json({message: {items: []}});
    throw new Error("Unexpected transport destination " + hostname);
  });
  const args = ["node", "batch", "--open-access", "--si", "--title", "中文论文", "--out", folder];
  await main([...args, "--pdf-url", "https://repository.test/paper.pdf"]);
  assert.deepEqual(destinations, ["repository.test"]);
  let manifest = JSON.parse(await readFile(join(folder, "manifest.json"), "utf8"));
  assert.equal(manifest.results[0].status, "open_access_downloaded");
  assert.equal(manifest.results[0].si.status, "not_checked");
  destinations.length = 0;
  await main(args);
  assert.deepEqual(destinations, ["export.arxiv.org", "api.crossref.org"]);
  manifest = JSON.parse(await readFile(join(folder, "manifest.json"), "utf8"));
  assert.equal(manifest.results[0].status, "oa_not_found");
});

async function cliFixture(t) {
  const folder = await mkdtemp(join(tmpdir(), "fulltext-routes-"));
  const previousDir = process.env.LIT_DL_CONFIG_DIR;
  process.env.LIT_DL_CONFIG_DIR = folder;
  t.after(async () => {
    if (previousDir === undefined) delete process.env.LIT_DL_CONFIG_DIR;
    else process.env.LIT_DL_CONFIG_DIR = previousDir;
    await rm(folder, { recursive: true, force: true });
  });
  t.mock.method(console, "log", () => {});
  return async (...args) => {
    await main(["node", "batch", "--out", folder, ...args]);
    return JSON.parse(await readFile(join(folder, "manifest.json"), "utf8"));
  };
}

test("failed arXiv PDF falls through once and remains in the manifest", async (t) => {
  const run = await cliFixture(t);
  const hosts = [];
  const pdf = "https://arxiv.org/pdf/2012.12345";
  const title = "Fixture title";
  let foundDoi = true;
  t.mock.method(globalThis, "fetch", async endpoint => {
    const { hostname, pathname } = new URL(endpoint);
    hosts.push(hostname);
    if (hostname === "export.arxiv.org") return new Response('<feed><entry><title>Fixture title</title><id>https://arxiv.org/abs/2012.12345</id></entry></feed>');
    if (hostname === "arxiv.org") return new Response("", {status: 404});
    if (hostname === "api.crossref.org" && pathname === "/works") return Response.json({message: {items: foundDoi ? [{
      DOI: "10.9999/test", title: [title], license: [{URL: "https://creativecommons.org/licenses/by/4.0/"}],
      link: [{"content-type": "application/pdf", URL: "https://publisher.test/open.pdf"}],
    }] : []}});
    if (hostname === "www.ebi.ac.uk") return Response.json({resultList: {result: []}});
    if (hostname === "api.unpaywall.org") return Response.json({is_oa: true, best_oa_location: {url_for_pdf: pdf}});
    if (hostname === "publisher.test") return new Response("%PDF-1.7 fixture", {headers: {"content-type": "application/pdf"}});
    throw new Error("Unexpected transport " + endpoint);
  });
  const args = ["--open-access", "--title", title, "--si", "--unpaywall-email", "fixture@example.test"];
  let manifest = await run(...args);
  const result = manifest.results[0];
  assert.equal(result.status, "open_access_downloaded");
  assert.equal(result.si.status, "not_checked");
  assert.equal(result.oaAttempts.length, 1);
  assert.equal(result.oaAttempts[0].url, pdf);
  assert.match(result.oaAttempts[0].reason, /404/);
  assert.deepEqual(hosts, ["export.arxiv.org", "arxiv.org", "api.crossref.org", "www.ebi.ac.uk", "api.unpaywall.org", "publisher.test"]);
  foundDoi = false;
  hosts.length = 0;
  manifest = await run(...args);
  assert.equal(manifest.results[0].status, "pdf_fetch_failed");
  assert.equal(manifest.results[0].oaAttempts[0].url, pdf);
  assert.deepEqual(hosts, ["export.arxiv.org", "arxiv.org", "api.crossref.org"]);
});

for (const stage of ["article", "nested", "OA nested", "attachment navigation", "attachment response", "partial handoff", "absent", "saved"]) {
  test("CLI reports the SI outcome and retains the main article: " + stage, async (t) => {
    const run = await cliFixture(t);
    t.mock.method(globalThis, "setTimeout", (callback) => queueMicrotask(callback));
    const article = "https://publisher.test/article";
    const nested = "https://publisher.test/supporting";
    const attachment = "https://publisher.test/appendix.pdf";
    const previousAttachment = "https://publisher.test/table.pdf";
    const pdf = Buffer.from("%PDF-1.7 fixture");
    const tab = "fixture-page";
    const metadataLookups = [];
    const visited = [];
    let location = article;
    let attachmentRequests = 0;
    const blockedStage = !["absent", "saved"].includes(stage);
    let closed = false;
    t.mock.method(globalThis, "fetch", async (endpoint, options) => {
      const { hostname, pathname } = new URL(endpoint);
      if (hostname === "api.crossref.org") {
        metadataLookups.push(pathname);
        return Response.json({message: {DOI: "10.9999/first", title: ["Fixture"],
          license: [{URL: "https://creativecommons.org/licenses/by/4.0/"}],
          link: [{"content-type": "application/pdf", URL: article + ".pdf"}],
        }});
      }
      if (hostname === "www.ebi.ac.uk") return Response.json({resultList: {result: []}});
      if (hostname === "api.unpaywall.org") return Response.json({});
      if (hostname === "publisher.test") {
        assert.equal(stage, "OA nested");
        return new Response(pdf, {headers: {"content-type": "application/pdf"}});
      }
      assert.equal(hostname, "proxy.test");
      if (pathname === "/targets") return Response.json([]);
      if (pathname === "/new") return Response.json({targetId: tab});
      if (pathname === "/close") { closed = true; return Response.json({}); }
      if (pathname === "/navigate") {
        location = options.body;
        visited.push(location);
        return Response.json({});
      }
      if (pathname === "/info") return Response.json({ready: "complete", title: "Fixture", url: location});
      assert.equal(pathname, "/eval");
      const code = options.body;
      if (code.includes("document.body?.innerText")) {
        const blocked = stage === "article" && visited.length && location === article
          || ["nested", "OA nested"].includes(stage) && location === nested
          || stage === "attachment navigation" && location === attachment;
        return Response.json({value: blocked ? "Verify you are human" : "Article"});
      }
      if (code.includes("meta[name=citation_pdf_url]")) return Response.json({value: JSON.stringify({
        url: article, cand: [article + ".pdf"], articleTitle: "Fixture", title: "Fixture", body: "Article",
      })});
      if (code.includes("a[href],button")) return Response.json({value: JSON.stringify(stage === "absent" ? [] : location === article
        ? [{text: "Supporting Information", href: nested}]
        : (stage === "partial handoff" ? [previousAttachment, attachment] : [attachment]).map(href => ({text: "Supplementary PDF", href}))) });
      if (code.includes("const r=await fetch(")) {
        if (code.includes(JSON.stringify(attachment))) {
          attachmentRequests++;
          if (stage === "attachment navigation") return Response.json({value: JSON.stringify({ok: false, err: "Failed to fetch"})});
          if (["attachment response", "partial handoff"].includes(stage)) {
            const html = new Response("<html><head><title>Check</title></head><body>Verify you are human</body></html>", {headers: {"Content-Type": "text/html"}});
            Object.defineProperty(html, "url", {value: attachment});
            const value = await runInNewContext(code, {fetch: async () => html, TextDecoder, window: {}, location: {href: nested}});
            return Response.json({value});
          }
          assert.equal(stage, "saved");
        }
        return Response.json({value: JSON.stringify({ok: true, status: 200, size: pdf.length, head: [...pdf], contentType: "application/pdf", url: article + ".pdf"})});
      }
      if (code.includes("return btoa(")) return Response.json({value: pdf.toString("base64")});
      if (code.startsWith("delete window")) return Response.json({});
      throw new Error("Unexpected browser interaction");
    });
    const routing = stage === "OA nested" ? [] : ["--route", "web_access"];
    const dois = blockedStage ? "10.9999/first,10.9999/second" : "10.9999/first";
    const manifest = await run(...routing, "--proxy", "https://proxy.test", "--dois", dois, "--si");
    assert.equal(manifest.results.length, 1);
    const result = manifest.results[0];
    assert.deepEqual(await readFile(result.file), pdf);
    assert.equal(metadataLookups.length, 1);
    if (!blockedStage) {
      assert.equal(result.si.status, stage === "saved" ? "downloaded" : "not_found");
      assert.equal(result.status, stage === "saved" ? "downloaded_with_si" : "downloaded");
      assert.equal(closed, true);
      if (stage === "saved") {
        assert.deepEqual(await readFile(result.si.files[0]), pdf);
        assert.match(result.si.files[0], /10\.9999_first__appendix\.pdf$/);
      }
      return;
    }
    assert.equal(result.status, stage === "OA nested" ? "open_access_downloaded" : "downloaded");
    assert.equal(result.si.status, "publisher_verification_waiting_user");
    assert.equal(result.si.tab, tab);
    assert.equal(result.si.url, stage === "article" ? article : stage.endsWith("nested") ? nested : attachment);
    assert.equal(attachmentRequests, stage.startsWith("attachment") || stage === "partial handoff" ? 1 : 0);
    if (stage === "partial handoff") {
      assert.equal(result.si.downloaded, 1);
      assert.deepEqual(await readFile(result.si.files[0]), pdf);
    }
    assert.equal(closed, false);
  });
}
