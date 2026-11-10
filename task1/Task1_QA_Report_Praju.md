# Task 1 — QA & Debug Report

**App under test:** Conduit (RealWorld) — https://demo.realworld.show/  
**Also checked:** https://demo.realworld.io/ (assignment-listed demo URL)  
**Tester:** Praju  
**Date:** 10 Nov 2026  
**Scope exercised:** Home feed, Sign up, Sign in, New Article, Publish, Delete Article, Your Feed, Tags sidebar  

> Note: The assignment’s public demo URL `https://demo.realworld.io` currently returns **404 NoSuchBucket**. Testing continued on the live Conduit demo at `https://demo.realworld.show/` (Angular frontend + RealWorld demo API).

---

## Bug table

| # | Title / Summary | Steps to Reproduce | Expected vs Actual | Severity | Suspected Cause |
|---|-----------------|--------------------|--------------------|----------|-----------------|
| 1 | Official RealWorld demo host is completely down | Open https://demo.realworld.io/ | **Expected:** Conduit demo loads. **Actual:** AWS S3-style `404 Not Found` / `NoSuchBucket` for bucket `demo.realworld.io`. | Critical | Hosting misconfiguration / deleted S3 bucket or broken DNS→bucket mapping for the public demo. |
| 2 | Delete Article has no confirmation | Sign in → open your article → click **Delete Article** | **Expected:** Confirm dialog before irreversible delete. **Actual:** Article deletes immediately and redirects home; no modal, no “Are you sure?”. | High | Delete handler calls API on click with no UX guard (`window.confirm` / modal) in the Angular article component. |
| 3 | Client-side validation is weak / bypassable | On `/register`, enter username `qa`, email `not-an-email`, password `1` → Sign up. Also open `/editor` and publish with empty fields. | **Expected:** Form blocks invalid email / weak password / blank article before API call, with clear field-level errors. **Actual:** Submit enabled for invalid email & 1-char password; form uses `novalidate`; Angular marks invalid email `ng-valid`; empty article only fails after server round-trip (`title/description/body can't be blank`). | High | Reactive form validators incomplete (no email/minLength validators); HTML5 validation disabled via `novalidate`. |
| 4 | Document title never changes across routes | Visit `/`, `/login`, `/register`, `/editor`, and an article URL; check browser tab title. | **Expected:** Title reflects page, e.g. “Sign in — Conduit”, article title. **Actual:** Always `Conduit`. | Medium | Angular `Title` service / route `title` metadata not configured. |
| 5 | Multiple H1 headings on feed and article pages | Open Global Feed; open an article whose body contains `# Heading` markdown. | **Expected:** One page-level H1; article list titles as H2/H3; markdown headings demoted or scoped. **Actual:** Each feed card title is an H1; markdown `#` inside body also becomes H1 → multiple H1s. | Medium | Semantic heading misuse in article preview template + markdown renderer emits raw H1. |
| 6 | Auth/error forms lack accessible labels & live regions | Inspect Sign up / Sign in / Editor / Comment inputs and error list after failed submit. | **Expected:** Visible `<label for>` associations; errors announced via `role="alert"` / `aria-live`. **Actual:** Inputs rely on placeholders only (0 `<label>` elements observed); `.error-messages` has no alert/live attributes. | Medium | Accessibility not implemented for forms; placeholder-as-label pattern. |
| 7 | Favorite control accessible name is only the count | On Global Feed, inspect favorite buttons with screen reader / a11y tree. | **Expected:** Name like “Favorite article (1)”. **Actual:** Accessible name is just `1` / `2`. | Low | Button text is only the favorites count; missing `aria-label`. |

**Evidence screenshots:** see `/screenshots/`  
- `01-empty-article-validation-errors.png` — server-only blank-field errors after Publish  
- `02-official-demo-realworld-io-404.png` — broken assignment demo host  

---

## Root-cause analysis (Issue #2 — Delete without confirmation)

When an author clicks **Delete Article**, the UI immediately issues a DELETE request for that article slug and then navigates to Home. There is no intermediate confirmation step, so a mis-click permanently removes content.

This almost certainly lives in the article detail component’s delete click handler: the button is wired directly to the articles API service (or store action) instead of opening a confirm dialog first. Because the demo also shows **two** Delete buttons (banner + footer), the accidental-click surface is doubled.

**Fix I would ship:**  
1) On click, open a confirm modal (“Delete this article? This cannot be undone.”) with Cancel / Delete.  
2) Only call the DELETE API after affirmative action; disable both buttons while the request is in flight.  
3) On failure, keep the article page and show an error toast.  
4) Optionally soft-delete or add a short undo snackbar for better recovery.

This is a classic “vibe-coded” gap: the happy path works, but destructive actions lack production-grade guardrails.

---

## Test notes / assumptions

- Session isolation on the demo API may reset data; bugs above were reproduced in a fresh browser session on 10 Nov 2026.  
- XSS payloads in titles/bodies appeared escaped/stripped (positive finding; not filed as a bug).  
- “Your Feed” empty state messaging works; tags sidebar briefly exposes conflicting “Loading tags… / No tags…” copy alongside loaded tags (minor race; not expanded above to keep the table focused).
