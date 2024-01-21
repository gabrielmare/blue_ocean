PARAMS = {
    "header": {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36"
    },
    "blackbox": {
        "format_date": "%d/%m/%Y",
        "wait_not_so_fast": {
            "enable": True,
            "seconds": {"min": 2, "max": 10},
            "next_stop": {"min": 40, "max": 70}
        },
        "default_dates": {
            "start": "",
            "end": "",
            "periods": 10
        }
    }
}
