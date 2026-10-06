# Project

**Name:** Deep Research Studio

**What it is:** A deep research tool. A user submits a question; the system runs a
real research workflow (plan -> search the live web -> synthesize -> write a cited
report) and streams every step back to the browser in real time.

**Who uses it:** People who want a transparent, multi-model alternative to a
black-box research assistant -- they can watch the thinking, switch models, and
compare models side by side.

**Core principles**
1. Bring your own key. The user supplies an OpenAI, Anthropic, or Kimi key per
   request. The server stores nothing.
2. Transparency. Every stage (planning, researching, report) streams live.
3. Multi-model. One question can run on any supported model, or several at once.

**Reference implementations copied for shape (not code):**
- Backend: https://github.com/ShenSeanChen/launch-DeepResearch-Backend
- Frontend: https://github.com/ShenSeanChen/launch-DeepResearch-Frontend

**Non-goals (this build):** accounts/auth, saved history server-side, billing,
vector stores. Keep the server stateless.
