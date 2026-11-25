# Output language pair

The task's abstract cardinality (bilingual, English only, or manuscript language only) is independent of its language pair. For bilingual output, an explicit supported pair takes precedence. With a Simplified Chinese manuscript use `zh-cn-en`; with Traditional Chinese use `zh-tw-en`. For English manuscripts without a specified Chinese variant the historical default is `zh-tw-en`.

<!-- output-language-pair-registry:start -->
| Token | L1 language | L1 script | L2 language | L2 script |
|-------|-------------|-----------|-------------|-----------|
| `zh-cn-en` | Simplified Chinese (zh-CN) | CJK | English (en) | Latin |
| `zh-tw-en` | Traditional Chinese (zh-TW) | CJK | English (en) | Latin |
<!-- output-language-pair-registry:end -->

Intake records the selected token in the Paper Configuration Record. Dispatch it to the outline, abstract and draft agents. Schema 4 retains `abstract: {english, chinese}` and selects the matching keyword key (`zh_cn` or `zh_tw`, alongside `en`). The simplified heading is `Chinese Abstract (zh-CN)`; the traditional writer preserves `Chinese Abstract`. Locale-qualified traditional headings are accepted on input. An older handoff without a token uses its recorded manuscript language; with no language information its historical Traditional Chinese headings and keys remain valid. Reject conflicting declarations and unsupported explicit values.

Use the [abstract writing guide](../roles/draft/paper/references/abstract_writing_guide.md) for counting units, venue overrides, and keywords per language.
