# Changelog

All notable changes to this project will be documented in this file.

## [1.0.0] - 2026-07-15
### Added
- Initial release of DryGram framework.
- Fully asynchronous client architecture supporting custom methods.
- Cryptographic engine supporting MTProto v2.0 DH key exchange and AES-IGE encryption.
- Network transport layers: Abridged, Intermediate, Padded Intermediate.
- Multi-engine session backends (SQLite, PostgreSQL, Redis, MongoDB, Memory).
- Event dispatcher system with priority queues, background workers, middleware pipelines, and custom gates.
- Extensive dataclass-based model definitions with Python 3.13 slot optimizations.
- Hot-reload plugin engine.
- Call stream integration module for voice/video.
