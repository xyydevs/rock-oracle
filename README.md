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
现在是立秋的第一天晚上，很晚，外面有很多的蝉在叫。
```

Possible answer:

```text
《Harvest Moon》 - Neil Young

风格：folk rock / acoustic rock
我听到的画面：立秋刚落下，夜还热着，蝉声像夏天最后一层没有退去的电流。
为什么是它：这首歌有秋天的名字，但声音不是萧瑟的，是温柔、慢、还带着一点夏夜的余温。
适合这样听：很晚的时候，开一点窗，让外面的蝉声和吉他一起进来。
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
└── agents
    └── openai.yaml
```

## License

No license has been selected yet. Add a license before treating this as reusable open-source software.
