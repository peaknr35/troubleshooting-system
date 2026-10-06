# Spec: Frontend (Next.js)

**Problem:** People need a clean, modern, mobile-friendly way to ask a question,
watch research stream in, switch models, compare models, and export results.

**Proposal:** A Next.js 15 App Router app with a chat-style interface and a
compare view, keys managed in the browser.

**Scope (in):**
- Chat-like input; live streaming of thinking / progress stages / sources
- Model switching (provider + model dropdown)
- Compare mode: same prompt across multiple models, results + timing side by side
- API key manager: enter, save (localStorage), import/export JSON, clear
- Research state persists across navigation (Context in root layout + storage)
- Export final report to Google Docs (copy-for-Docs + optional OAuth create)
- Responsive, accessible, works on mobile and desktop

**Scope (out):** server-side accounts, SSR of research results (results are
client-streamed), design-system theming beyond Tailwind.

**Dependencies:** `_shared/api-contract.md` (event shape), `_shared/providers.md`
(model catalog), backend `NEXT_PUBLIC_BACKEND_URL`.
