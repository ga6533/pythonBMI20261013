---
name: create-user-story-and-ac
description: "Create or complete User Story and Acceptance Criteria for GitHub Project work items. Use when reviewing a Project's Ready column, when an issue lacks a User Story or Acceptance Criteria, or when acceptance criteria must be written as a Markdown checklist."
argument-hint: "Specify a GitHub Project URL, or use the currently open Project page."
user-invocable: true
disable-model-invocation: false
---

# Create User Story and Acceptance Criteria

## Purpose

Review work items in a GitHub Project's **Ready** column and add missing requirements to the linked issue. Keep existing content intact unless it is clearly only a placeholder or the user explicitly requests a rewrite.

## Procedure

1. Open the supplied GitHub Project URL, or use the currently shared Project page.
2. Confirm that the page is accessible and that the user is authenticated. Never request or handle the user's GitHub password or authentication codes.
3. Identify every item in the **Ready** column. Record each item's issue number, title, and linked repository.
4. Open each work item and inspect its issue description.
5. Determine independently whether the description contains:
   - a meaningful **User Story**, normally phrased as "As a ... I want ... so that ..."; and
   - meaningful **Acceptance Criteria** describing observable, testable outcomes.
6. If either section is missing, infer requirements from the issue title, existing description, labels, linked work, and the repository's domain. Do not invent unrelated scope.
7. Update the issue description while preserving useful existing text. Use this structure:

   ```markdown
   ## User Story

   As a [user or role], I want [capability], so that [benefit].

   ## Acceptance Criteria

   - [ ] [Observable, testable criterion]
   - [ ] [Observable, testable criterion]
   ```

8. Write every acceptance criterion as an unchecked Markdown checklist item using `- [ ]`. Criteria should cover the happy path, validation or error handling where relevant, and the expected result.
9. Save the issue, then reopen or refresh it to verify that both headings and checklist items are rendered correctly.
10. Report which Ready items were changed and which were already complete. Do not claim an update succeeded without verifying it.

## Quality Rules

- Write requirements in the language and terminology used by the work item; use Traditional Chinese when the work item is Chinese.
- Make criteria specific enough to verify manually or with tests.
- Avoid implementation details unless they are part of the stated requirement.
- Do not mark checklist items complete; they describe acceptance conditions.
- If the Project is inaccessible, stop and ask the user to authenticate or share the correct page.
