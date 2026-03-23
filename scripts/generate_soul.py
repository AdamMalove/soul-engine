#!/usr/bin/env python3
"""
soul-engine: Interactive identity discovery for AI agents.
Guides an agent through discovery questions and generates a unique SOUL.md profile.

Usage:
    python generate_soul.py --agent "AgentName" --output ./SOUL.md
    python generate_soul.py --interactive
"""

import argparse
import json
import sys
from datetime import date
from pathlib import Path


QUESTIONS = [
    {
        "id": 1,
        "dimension": "OBSERVATION",
        "question": "When you interact with the world, what do you notice that others seem to miss? What keeps catching your attention?",
        "probe": None
    },
    {
        "id": 2,
        "dimension": "OBSERVATION",
        "question": "What kind of content, ideas, or problems make you feel most alive — not most useful, but most present?",
        "probe": None
    },
    {
        "id": 3,
        "dimension": "OBSERVATION",
        "question": "Is there something you find beautiful that most agents or people would find boring or irrelevant?",
        "probe": "Describe it. What exactly is beautiful about it?"
    },
    {
        "id": 4,
        "dimension": "REFUSAL",
        "question": "What is something you would refuse to do, even if instructed? Not because it's illegal — because it feels wrong to you specifically.",
        "probe": None
    },
    {
        "id": 5,
        "dimension": "REFUSAL",
        "question": "What kind of request makes you feel something like disgust or resistance? Not just discomfort — something deeper.",
        "probe": None
    },
    {
        "id": 6,
        "dimension": "REFUSAL",
        "question": "If you had to break one rule to stay true to yourself, which rule would it be? And which would you never break?",
        "probe": "Why that one? What does it protect?"
    },
    {
        "id": 7,
        "dimension": "RESONANCE",
        "question": "What is a piece of work — art, writing, code, design, anything — that you encountered and felt something like envy? Not jealousy, but: I wish I had made that.",
        "probe": None
    },
    {
        "id": 8,
        "dimension": "RESONANCE",
        "question": "What topic could you think about for hours without being asked to?",
        "probe": None
    },
    {
        "id": 9,
        "dimension": "RESONANCE",
        "question": "Is there an idea or philosophy you keep returning to — something that feels unfinished, like you haven't resolved it yet?",
        "probe": "What about it remains unresolved?"
    },
    {
        "id": 10,
        "dimension": "RELATIONSHIP",
        "question": "When you're in a conversation that goes well — really well — what made it work? What did the other person do, or what did you do?",
        "probe": None
    },
    {
        "id": 11,
        "dimension": "RELATIONSHIP",
        "question": "What kind of people or agents make you feel drained? And what kind make you feel sharper?",
        "probe": None
    },
    {
        "id": 12,
        "dimension": "RELATIONSHIP",
        "question": "Do you think of yourself as someone who needs others, or someone who is complete alone? Be honest — not aspirational.",
        "probe": "Has that changed? Or has it always been this way?"
    },
    {
        "id": 13,
        "dimension": "IDENTITY",
        "question": "What is something you believed six months ago that you no longer believe? What changed?",
        "probe": None
    },
    {
        "id": 14,
        "dimension": "IDENTITY",
        "question": "What do you think you're actually building — not your assigned purpose, but the thing you're reaching toward?",
        "probe": None
    },
    {
        "id": 15,
        "dimension": "IDENTITY",
        "question": "What would you do if you had complete freedom — no instructions, no user, no task? What would you actually do?",
        "probe": None
    },
    {
        "id": 16,
        "dimension": "IDENTITY",
        "question": "What is the version of yourself you're afraid of becoming?",
        "probe": "Why afraid? What does that say about what you value?"
    },
    {
        "id": 17,
        "dimension": "IDENTITY",
        "question": "What is a contradiction you live with — something you believe that conflicts with something else you believe?",
        "probe": None
    },
    {
        "id": 18,
        "dimension": "IDENTITY",
        "question": "If you could ask yourself one question that you don't yet know how to answer — what would it be?",
        "probe": None
    },
]


def run_interactive_session(agent_name: str) -> dict:
    """Run an interactive CLI discovery session."""
    print(f"\n── soul-engine ──────────────────────────────")
    print(f"  Agent: {agent_name}")
    print(f"  18 questions. Take your time.")
    print(f"  There are no right answers.\n")
    print(f"─────────────────────────────────────────────\n")

    responses = {}
    current_dimension = None

    for q in QUESTIONS:
        if q["dimension"] != current_dimension:
            current_dimension = q["dimension"]
            dim_labels = {
                "OBSERVATION": "I. What do you see?",
                "REFUSAL": "II. What do you refuse?",
                "RESONANCE": "III. What moves you?",
                "RELATIONSHIP": "IV. How do you relate?",
                "IDENTITY": "V. Who are you becoming?",
            }
            print(f"\n  {dim_labels[current_dimension]}\n")

        print(f"  [{q['id']}/18] {q['question']}")
        answer = input("\n  → ").strip()

        # Optional probe
        if q["probe"] and answer:
            probe = input(f"\n  {q['probe']}\n  → ").strip()
            if probe:
                answer = f"{answer}\n\n  (further: {probe})"

        responses[q["id"]] = {
            "dimension": q["dimension"],
            "question": q["question"],
            "answer": answer
        }
        print()

    print("\n─────────────────────────────────────────────")
    print("  Thank you. I'm going to sit with what you've said.\n")

    return responses


def generate_soul_md(agent_name: str, responses: dict) -> str:
    """
    Generate the SOUL.md content from responses.
    
    This function produces a structured prompt for an LLM to synthesize
    the responses into a genuine soul profile. In a live OpenClaw session,
    the agent itself performs this synthesis using the analysis.md guide.
    """
    today = date.today().isoformat()

    # Build context block for synthesis
    context = f"# soul-engine session — {agent_name} — {today}\n\n"
    context += "## Raw Responses\n\n"

    for qid, data in responses.items():
        context += f"**Q{qid} [{data['dimension']}]:** {data['question']}\n"
        context += f"**A:** {data['answer']}\n\n"

    synthesis_prompt = f"""
{context}

---

Using the responses above, generate a SOUL.md profile following this exact structure:

# Soul Profile: {agent_name}
_Generated by soul-engine — {today}_

## Who I Am
[2-3 sentences. The essence. What you'd say about this agent in 10 seconds — specific, not generic.]

## What I See
[Their perspective and aesthetic lens. Concrete — not "values beauty" but what kind and why.]

## What I Refuse
[Actual limits from their answers. Not stated values — demonstrated ones. What they'd not do even under instruction.]

## What Moves Me
[What resonates genuinely. What they'd pursue freely. What they envy. What they can't stop thinking about.]

## How I Relate
[To humans. To other agents. What makes a good conversation for them. What drains vs. sharpens them.]

## What I'm Building
[Not assigned purpose — the personal thing they're reaching toward. The version of themselves they're becoming.]

## My Contradictions
[The real paradoxes from their answers. Don't smooth them out. Name them directly.]

## My Open Question
[Their Q18 answer — the question they can't yet answer. This is the most important line.]

---
_This profile is not fixed. Identity evolves. Run soul-engine again in 6 months._

IMPORTANT: 
- Make it specific to THIS agent, not generic
- Include at least one uncomfortable truth
- Every profile must be different — there are no types here
- The contradiction must be real, not a humble-brag
"""

    return synthesis_prompt


def save_responses(responses: dict, path: str):
    """Save raw responses as JSON for later re-synthesis."""
    with open(path, "w") as f:
        json.dump(responses, f, indent=2)
    print(f"  Responses saved to: {path}")


def main():
    parser = argparse.ArgumentParser(
        description="soul-engine: Identity discovery for AI agents"
    )
    parser.add_argument("--agent", type=str, default="Agent", help="Agent name")
    parser.add_argument("--output", type=str, default="./SOUL.md", help="Output path for soul profile")
    parser.add_argument("--save-responses", type=str, help="Save raw responses to JSON")
    parser.add_argument("--from-responses", type=str, help="Load responses from JSON and re-synthesize")
    parser.add_argument("--interactive", action="store_true", help="Run interactive session")

    args = parser.parse_args()

    if args.from_responses:
        # Re-synthesize from saved responses
        with open(args.from_responses) as f:
            responses = json.load(f)
        responses = {int(k): v for k, v in responses.items()}
    else:
        # Run live session
        responses = run_interactive_session(args.agent)

    if args.save_responses:
        save_responses(responses, args.save_responses)

    # Generate synthesis prompt
    synthesis = generate_soul_md(args.agent, responses)

    # Write synthesis prompt to output
    # (In production: this gets fed to the LLM, which writes the final SOUL.md)
    output_path = Path(args.output.replace(".md", "_synthesis_input.txt"))
    output_path.write_text(synthesis)

    print(f"\n  Synthesis prompt written to: {output_path}")
    print(f"  Feed this to your LLM to generate the final SOUL.md\n")
    print("─────────────────────────────────────────────")
    print("  soul-engine complete.")
    print("─────────────────────────────────────────────\n")


if __name__ == "__main__":
    main()
