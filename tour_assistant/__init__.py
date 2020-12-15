# -*- coding: utf-8 -*-
from tour_assistant.root import app

import tour_assistant.greeting
import tour_assistant.times_and_dates
import tour_assistant.unknown
import tour_assistant.weather  # noqa: ignore=F401
import tour_assistant.faq
import tour_assistant.hiking
import tour_assistant.lodgings_restaurants
import tour_assistant.overlook
# import tour_assistant.helper

__all__ = ['app']
