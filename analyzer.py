# python3
# tdolega

import json, re, collections, math

# otworzenie pliku z wiadomościami
# plik musi się nazywać message.json i znajdować w tym samym katalogu
with open('message.json') as f:
    data = json.load(f)
messages = data["messages"]

# każdy uczestnik dostaje swoją instancję
class Participant:

    static_messages_counter = 0
    static_photos_counter = 0

    def __init__(self, name):
        self.messages_counter = 0
        self.photos_counter = 0
        self.name = name
        self.combined_messages = ""

    def fixStrings(self):
        self.combined_messages = fu(self.combined_messages)
        self.name = fu(self.name)

    # analizujemy wiadomość
    def handleMessage(self, m):
        if "content" in m:
            self.messages_counter += 1
            Participant.static_messages_counter += 1
            self.combined_messages += " " + m["content"]

        elif "photos" in m:
            self.photos_counter += 1
            Participant.static_photos_counter += 1


# keeping track of participants
participants = {}
def getParticipant(sender_name):
    if sender_name not in participants:
        p = Participant(sender_name)
        participants[sender_name] = p
    return participants.get(sender_name)

# fuck unicode - zwraca naprawiony string
def fu(broken_string):
    # TODO dodać duże litery, a najlepiej załatwić to wgl w lepszy sposób obsługujący wszystkie litery i co ważne emotikonki, to problem z unicode, pewnie ktoś już to rozwiazał
    # TODO obsługa polskich liter w rankingu ze słownika pod tym komentarzem
    unicode_to_utf8 = {
        "\u00c4\u0085":"ą",
        "\u00c5\u0082":"ł",
        "\u00c5\u0084":"ń",
        "\u00c4\u0099":"ę",
        "\u00c5\u00bc":"ż",
        "\u00c4\u0087":"ć",
        "\u00c5\u009b":"ś",
        "\u00c3\u00b3":"ó"
    }
    unicode_to_utf8 = {
        "\u00c4\u0085":"a",
        "\u00c5\u0082":"l",
        "\u00c5\u0084":"n",
        "\u00c4\u0099":"e",
        "\u00c5\u00bc":"z",
        "\u00c4\u0087":"c",
        "\u00c5\u009b":"s",
        "\u00c3\u00b3":"o"
    }
    for k, v in unicode_to_utf8.items():
        broken_string = broken_string.replace(k, v)
    return broken_string

# rysowanie rankingu słów
# TODO filtrowanie samych rzeczowników (użycie słownika online?)
def graph_rank(text_data):
    ignore = "na no sie w ale z o bo i a ze za se to co do ma p d po od"
    words_rank = collections.Counter([w for w in re.findall("[a-z]+",text_data.lower())if w not in ignore.split()]).most_common(25)
    print('\n'.join('|' + 76 * v // words_rank[0][1] * '_' + '| ' + k for k,v in words_rank))

# print ( ranking liczbowy )
def num_rank(rank_dict):
    rank_dict = [(k, rank_dict[k]) for k in sorted(rank_dict, key=rank_dict.get, reverse=True)]
    for k, v in rank_dict:
        print("", v, u"⇐", fu(k))
    print()

# rysowanie stringu w jakby ramce
def fancy_border_print(string):
    print("━" * 52)
    side_bar_len = int((50 - math.ceil(len(string))) / 2)
    print("━" * side_bar_len, string, "━" * (side_bar_len + len(string) % 2))
    print("━" * 52)

# przypisujemy wiadomość do instancji uczestnika
for m in messages:
    p = getParticipant(m["sender_name"])
    p.handleMessage(m)

# budowa rankingów
messages_rank = {}
messages_len_rank = {}
photos_rank = {}
for p in participants.values():
    p.fixStrings()
    messages_rank[p.name] = p.messages_counter
    try:
        messages_len_rank[p.name] = round(len(p.combined_messages) / p.messages_counter)
    except ZeroDivisionError:
        messages_len_rank[p.name] = 0
    photos_rank[p.name] = p.photos_counter

# wyświetlanie rankingów globalnych
print()
print("Łącznie wysłaliście sobie", Participant.static_messages_counter, "wiadomości:")
num_rank(messages_rank)
print("Średnia ilość znaków w wiadomości:")
num_rank(messages_len_rank)
print("Wysłano", Participant.static_photos_counter, "zdjęć:")
num_rank(photos_rank)

# wyświetlanie rankingów personalnych
for p in participants.values():
    fancy_border_print(fu(p.name))
    print("━" * 3, "Najczęściej używane słowa:")
    graph_rank(p.combined_messages)

    # TODO ranking emotikonek
    # inne pomysły:
    # - kto częściej zaczynał konwersację
    # - kto wysłał więcej serduszek :,)
    # Liczę na pomysły!
