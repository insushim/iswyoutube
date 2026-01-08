# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.0.0] - 2024-01-01

### Added
- Complete rewrite of video generation pipeline
- AI-powered topic generation with trend analysis
- Multi-style support (kurzgesagt, veritasium, vsauce, 3blue1brown, knowledge_pirate)
- YouTube Shorts automatic generation
- Multi-language support (ko, en, ja, zh, es)
- Thumbnail A/B testing with CTR prediction
- Community management (comment analysis, auto-response)
- Monetization optimization (ad placement, mid-roll detection)
- Series generation with continuity checking
- Content repurposing (blog, social media snippets)
- Backup and recovery system
- Docker support
- Comprehensive test suite
- Full documentation

### Changed
- Migrated to async/await architecture
- Updated to Python 3.10+
- Switched to Anthropic Claude for AI generation
- Improved TTS quality with ElevenLabs
- Enhanced image generation with DALL-E 3

### Removed
- Legacy synchronous API
- Deprecated Python 3.8 support

## [1.0.0] - 2023-06-01

### Added
- Initial release
- Basic video generation
- Simple TTS integration
- YouTube upload support
