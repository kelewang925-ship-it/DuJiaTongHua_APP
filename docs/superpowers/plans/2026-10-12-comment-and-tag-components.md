# Comment avatars and tag management

Reuse shared Avatar in diary/photo comment author rows. Keep the adjacent readable author name and hide the redundant avatar from assistive reading. Add an action mode to shared Tag (selected:null,onActivate) for existing tag edit/delete menus; default selectable Tag behavior stays unchanged. Use shared Divider between personal/shared groups. Preserve existing persistence, actions and illustrated canvas headers.

- [x] Capture real component adoption baseline.
- [x] Implement author rows, action tags and section divider.
- [x] Verify five widths and actual comment failure/retry plus tag edit/cancel; default/action Tag contracts.
- [x] Record header/original-art preservation decisions and remaining global scope; commit.

Task extends existing UI renderers. Header factory is already used in the corrupt-auth recovery view; original artwork headers need explicit per-page mapping rather than inserting a second header. No final acceptance is claimed.

Actual6464 exit1:1/5 baseline;37464 exit1:12/17 (five wrong tag-count assertions);34513 exit0:5 fresh+12 retained=17/17. Source frozen between last two executions.390px screenshots captured via actual reply/tag fixtures and visually inspected; all114 original h1 preserved in static decision table, no final acceptance.
