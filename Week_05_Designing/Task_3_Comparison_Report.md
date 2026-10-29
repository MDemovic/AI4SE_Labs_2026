# Task 3 — Comparing the discussion with and without the skill

## Without the skill

In the first session, I asked about the three architectures and their advantages / disadvantages, maintenance, how the code could become tangled, and whether serverless would reduce infrastructure management. I chose a modular monolith with managed hosting because microservices seemed like overkill and the maintenance looked manageable with proper discipline.

The first ADR still needed some clarification, mainly
- module boundary rules
- how a separate worker fits with one deployable application
- separation between architecture decisions and implementation details.

## With the skill

In the fresh session, the AI followed a more structured process. It compared the three options, asked about the first-release ticket scope and backend preference, and then recommended a modular monolith. I confirmed browsing and saving tickets only, with no purchase flow, and no established backend preference.

The resulting ADR already included concrete module rules, the optional worker's relationship to the main application, and details that could be finalized later. These were the things I had needed to point out in the first run, so the skill seems to have helped carry those lessons into the next session.

Both runs reached a similar architecture, but they were not same. In the first run, I accepted managed hosting as part of the approach. In the second, hosting remained open. The second run also made the no-purchase scope explicit, while the original ADR still listed purchasing as an unresolved question.

## What improved, and what did not

The skill made the output more complete from the start and reduced the need to repeat my earlier ADR feedback. The discussion was also easier to follow because it asked about missing requirements before treating them as decisions. Also the whole process was much faster.

However, the new documents were quite long and repetitive, especially about what had and had not been accepted. A shorter version would have been easier to review.

Also, my answers in the second discussion were mainly selections from options presented (usually 3-4 options). That is why they much more formal, so it again makes it harder to read. Also this could be an issue, if the selected interpretation is wrong, or rather that the option doesnt fully explain how the AI percieves it.

## Did it save time?

Absolutly, I did not track it but I think it took about an hour less for the whole process, but it is also true that in the second run I understood most of the architectural design patters. 

This was only one comparison. I also asked the original conversation for help interpreting the second session's choices, so it was not a completely independent test. The two runs had different clarifications and different styles of interaction. Overall, the skill was useful for making the process more consistent, but the result could still be more concise.

## Files

- Original [discussion](Task_1_Discussion_Notes.md) and [ADR](Task_2_Architecture_Decision_Record.md).
- Reusable [skill](SKILL.md).
- Skill-assisted [discussion](AI_result/discussion.md) and [ADR](AI_result/ADR-0001-onesport-architecture.md).
