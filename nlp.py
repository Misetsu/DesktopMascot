import spacy
import ginza
import pendulum
from ja_timex.timex import TimexParser

KEYS = ["アラーム", "日記", "タスク", "メモ"]


class NlpProcess:

    def getKeyword(self, target):
        global KEYS
        nlp = spacy.load("ja_ginza")
        doc = nlp(target)
        li_keyword = [i.text for i in ginza.bunsetu_phrase_spans(doc)]
        action = 0
        for i in range(len(KEYS)):
            if KEYS[i] in li_keyword:
                action = i + 1
                break
        li_time = self.getTime(target)
        return action, li_time, li_keyword

    def getTime(self, target):
        li_time = []
        timex_parser = TimexParser(reference=pendulum.now(tz="Asia/Tokyo"))
        timexes = timex_parser.parse(target)

        for i in range(len(timexes)):
            if timexes[i].type == "DATE":
                d = timexes[i].to_datetime().strftime("%Y%m%d")
                li_time.append(d)
            elif timexes[i].type == "TIME":
                t = timexes[i].to_datetime().strftime("%H:%M")
                li_time.append(t)
            elif timexes[i].type == "DURATION":
                t = timexes[i].to_datetime().strftime("%H:%M")
                nowt = pendulum.now(tz="Asia/Tokyo").strftime("%H:%M")
                if t == nowt:
                    d = timexes[i].to_datetime().strftime("%Y%m%d")
                    li_time.append(d)
                else:
                    t = timexes[i].to_datetime().strftime("%H:%M")
                    li_time.append(t)
        return li_time
