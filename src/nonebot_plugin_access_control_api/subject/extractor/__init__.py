from collections.abc import Sequence

from nonebot import Bot, logger
from nonebot.internal.adapter import Event

from ..manager import SubjectManager
from .base import T_SubjectExtractor
from .chain import SubjectExtractorChain

extractor_chain = SubjectExtractorChain()


def add_subject_extractor(extractor: T_SubjectExtractor) -> T_SubjectExtractor:
    extractor_chain.add(extractor)
    return extractor


def extract_subjects(bot: Bot, event: Event) -> Sequence[str]:
    manager = SubjectManager()
    extractor_chain(bot, event, manager)
    sbj = [x.content for x in manager.subjects]
    logger.debug("subjects: " + ", ".join(sbj))
    return sbj


__all__ = (
    "T_SubjectExtractor",
    "add_subject_extractor",
    "extract_subjects",
)
