"""Answer protection for offline assignments.

Answers are stored only as salted scrypt digests, the same technique used for
password storage: the client re-hashes a student's answer and compares.
The item id is part of the salt, so identical answers in two items produce
different digests and do not reveal that they are equal.

Limitation: items with few possible answers (quiz options, matching pairs)
can still be enumerated through the hash. The slow KDF raises the effort of
doing so, but no offline scheme can prevent it.
"""

import hashlib
import hmac
import re
import secrets
import unicodedata
from typing import Final

from word_games.assignment.model import ScryptParams, SealedAnswerKey
from word_games.game.model import Answer, AnswerKey, ItemId


_SALT_BYTES: Final[int] = 16
_DIGEST_BYTES: Final[int] = 32
_SCRYPT_MAX_MEMORY: Final[int] = 64 * 1024 * 1024


def normalize_answer(answer: Answer) -> str:
    whitespace_normed = re.sub(r"\s+", " ", answer.strip())
    return unicodedata.normalize("NFKC", whitespace_normed).casefold()


def digest_answer(
    answer: Answer, item_id: ItemId, salt: bytes, params: ScryptParams
) -> bytes:
    return hashlib.scrypt(
        normalize_answer(answer).encode(),
        salt=salt + item_id.encode(),
        n=params.n,
        r=params.r,
        p=params.p,
        maxmem=_SCRYPT_MAX_MEMORY,
        dklen=_DIGEST_BYTES,
    )


def seal_answer_key(
    answer_key: AnswerKey, params: ScryptParams | None = None
) -> SealedAnswerKey:
    params = params or ScryptParams()
    salt = secrets.token_bytes(_SALT_BYTES)
    digests = {
        item_id: digest_answer(answer, item_id, salt, params).hex()
        for item_id, answer in answer_key.items()
    }
    return SealedAnswerKey(salt=salt.hex(), params=params, digests=digests)


def is_answer_correct(
    sealed: SealedAnswerKey, item_id: ItemId, answer: Answer
) -> bool:
    expected = sealed.digests.get(item_id)
    if expected is None:
        return False
    actual = digest_answer(
        answer, item_id, bytes.fromhex(sealed.salt), sealed.params
    )
    return hmac.compare_digest(actual, bytes.fromhex(expected))
