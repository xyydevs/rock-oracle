# Rock Oracle

Rock Oracle is a Codex skill that maps a user's intention, mood, image, or scene into exactly one rock or rock-adjacent song recommendation.

It is designed less like a streaming recommendation algorithm and more like a tasteful, slightly unpredictable rock DJ: it listens for the moment, makes one choice, and explains the choice with restraint.

## What It Does

- Recommends exactly one song.
- Prioritizes rock and rock-adjacent styles: classic rock, folk rock, acoustic rock, alternative, indie rock, punk, post-punk, grunge, shoegaze, post-rock, slowcore, dream pop, and nearby forms.
- Interprets concrete scenes as well as explicit music requests.
- Distinguishes between present moments, memories, desires, and hypothetical scenes.
- Uses user feedback to recalibrate the current exchange without building a long-term taste profile.
- Preserves surprise instead of over-personalizing.
- Uses MusicBrainz for existence checks when web/API access is available.

## Example

User:

```text
I am on a train leaving a city I do not hate. The sky is turning orange, and my headphones feel like a private room.
```

Possible answer:

```text
《There Is a Light That Never Goes Out》 - The Smiths

风格：jangle pop / alternative rock
我听到的画面：火车离站，窗外的城市在夕阳里变成一排会发光的旧念头。
为什么是它：这首歌有离开的冲动，但不是干脆的告别；它更像把浪漫、疲惫和一点自我戏剧化塞进同一副耳机里。
适合这样听：列车刚加速、站台灯光开始往后退的时候。
```

## Installation

Copy this skill folder into your Codex skills directory:

```bash
mkdir -p ~/.codex/skills
cp -R rock-oracle ~/.codex/skills/
```

Then start a new Codex session and invoke it explicitly:

```text
Use $rock-oracle: 我刚下班走出写字楼，外面下雪了。
```

Depending on your Codex setup, the skill may also be invoked implicitly when you ask for a song recommendation from a mood, scene, or intention.

## Design Principles

Rock Oracle follows a few rules:

- Current scene first, not keyword matching.
- One song, not a playlist.
- Rock first, but with a wide rock-adjacent vocabulary.
- Explanation should be vivid but controlled.
- User corrections are local calibration, not permanent personalization.
- Surprise is part of the experience.

## Verification

The skill can use MusicBrainz to check that a recommended song exists when web/API access is available. MusicBrainz is used only for existence checking and light metadata, not to drive the aesthetic choice.

If verification is unavailable, the skill should fall back to high-confidence music knowledge instead of stalling.

## Boundaries

This skill does not:

- Store or quote full copyrighted lyrics.
- Download audio.
- Provide playback links by default.
- Manage Spotify, NetEase Cloud Music, YouTube, or other playback services.
- Maintain a long-term taste profile unless explicitly extended to do so.

## Repository Contents

```text
.
├── SKILL.md
├── agents
│   └── openai.yaml
└── scripts
    └── verify_musicbrainz.py
```

## License

No license has been selected yet. Add a license before treating this as reusable open-source software.
