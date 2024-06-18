import tgt

MAX_DUR = 4

def split_textgrid(tg_path, basename):
    tg = tgt.read_textgrid(tg_path, include_empty_intervals=True)
    phones_tier = None
    for tier in tg.tiers:
        if tier.name == "phones":
            phones_tier = tier
            break
    if phones_tier is None:
        print("Error: Tier 'phones' not found in the TextGrid.")
        return

    offset_start = 0
    while offset_start < tg.end_time:
        offset_end = min(offset_start + MAX_DUR, tg.end_time)
        tg_part = tgt.TextGrid()
        intr_part = []

        for ann in phones_tier:
            if ann.end_time <= offset_start or ann.start_time >= offset_end:
                continue
            start_time_adjusted = max(ann.start_time, offset_start) - offset_start
            end_time_adjusted = min(ann.end_time, offset_end) - offset_start
            new_ann = tgt.Interval(start_time_adjusted, end_time_adjusted, ann.text)
            intr_part.append(new_ann)
        tier_part = tgt.IntervalTier(name=phones_tier.name, start_time=0, end_time=offset_end - offset_start, objects=intr_part)
        tg_part.add_tier(tier_part)
        outpath = f"../{basename}/{basename}_{int(offset_start//MAX_DUR)}.TextGrid"
        tgt.write_to_file(tg_part, outpath, format="long")

        offset_start += MAX_DUR

