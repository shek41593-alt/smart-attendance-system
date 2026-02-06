from datetime import datetime

def get_current_subject():
    now = datetime.now()
    day = now.strftime("%A")   # Monday, Tuesday, etc
    hour = now.hour
    minute = now.minute

    time_in_minutes = hour * 60 + minute

    timetable = {
        "Monday": [
            (540, 595, "RER"),   # 09:00–09:55
            (780, 835, "IKS"),   # 01:00–01:55
            (835, 885, "ML"),    # 01:55–02:45
            (895, 940, "BCT")    # 02:55–03:40
        ],
        "Tuesday": [
            (540, 595, "ML"),
            (835, 885, "CC")
        ],
        "Wednesday": [
            (540, 595, "BCT"),
            (780, 835, "ML")
        ],
        "Thursday": [
            (540, 595, "ML"),
            (595, 650, "RER"),
            (650, 705, "CC"),
            (1320, 1375, "BCT"),
            (1375, 1430, "CC")
        ],
        "Friday": [
            (540, 595, "CC"),
            (780, 835, "BCT"),
            (835, 885, "RER")
        ],
        "Saturday": [
            (540, 595, "BCT"),
            (595, 650, "ML"),
            (650, 705, "CC")
        ]
    }

    if day not in timetable:
        return None

    for start, end, subject in timetable[day]:
        if start <= time_in_minutes <= end:
            return subject

    return None
