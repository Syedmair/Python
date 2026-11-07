def longest_unique_window(text):
    last_seen = {}      
    left = 0           
    best_start = 0
    best_len = 0

    for right, ch in enumerate(text):
        if ch in last_seen and last_seen[ch] >= left:
            left = last_seen[ch] + 1
        last_seen[ch] = right

        window_len = right - left + 1
        if window_len > best_len:
            best_len = window_len
            best_start = left

    return text[best_start:best_start + best_len], best_start, best_len