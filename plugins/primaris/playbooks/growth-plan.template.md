# Growth Plan — Template

> Living document. Edit this file when targets shift. Cawl reads it to align weekly recommendations.
>
> **First run**: copy this file to `$PRIMARIS_HOME/growth-plan.md` (default `~/.primaris/growth-plan.md`) and fill in the placeholders. Do **not** edit the template in-place — it is read-only and shipped with the plugin.
>
> ```bash
> mkdir -p ~/.primaris/eval
> cp plugins/primaris/playbooks/growth-plan.template.md ~/.primaris/growth-plan.md
> $EDITOR ~/.primaris/growth-plan.md
> ```

**Owner**: <your name or handle>
**Last updated:** <YYYY-MM-DD>

---

## Current state

- **Level:** <current level — Level 0..5 from `playbooks/ai-engineering-levels.md`>
- **Strongest evidence base:** <pull from `/insights` "Impressive Things You Did" section>
- **Weakest evidence base:** <pull from `/insights` "Where Things Go Wrong" section>

## Strengths to preserve

- <bullet — concrete behaviour you do reliably; cite the `/insights` section if available>
- <bullet>
- <bullet>

## Weaknesses to fix

- **<weakness label>.** <one-sentence description>. <forward link if Phase 2/3/4 will mechanise the fix>
- **<weakness label>.** <one-sentence description>.
- **<weakness label>.** <one-sentence description>.

## 30-day targets (review by <YYYY-MM-DD>)

- <numeric target — e.g. ≥80% of bug tickets prove root cause before first edit>
- <numeric target>
- <numeric target>
- <numeric target>
- <numeric target>

## 90-day targets (review by <YYYY-MM-DD>)

- <numeric target — typically the next-level capability checklist>
- <numeric target>
- <numeric target>
- <numeric target>

## Cawl's working assumptions

When scoring, Cawl should treat the following as your stable preferences (do not flag as anti-signals):

- <example: language convention — primary user-language for prose, English for code/commits>
- <example: communication style — terse / verbose / specific compression mode>
- <example: workflow preference — manual commit vs. auto-commit, single-PR vs. multi-PR refactors>
- <example: tolerance threshold — N tenet violations per week is "neutral" rather than "falling">

Add or remove items as your preferences solidify. Cawl re-reads this file every run.
