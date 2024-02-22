level_data = [
    {
        "tiles": [
            {"type": "2","start_x": 0,"start_y": 400,"iterations": 100,"direction": "increment","amount": 50},
            {"type": "5","start_x": 0,"start_y": 450,"iterations": 100,"direction": "increment","amount": 50},
            {"type": "2","start_x": 850,"start_y": 300,"iterations": 7,"direction": "increment","amount": 50},
            {"type": "2","start_x": 1260,"start_y": 190,"iterations": 7,"direction": "increment","amount": 50},
        ],
        "coins": [
            {"start_x": 50,"start_y": 350,"iterations": 15,"direction": "increment","amount": 30},
            {"start_x": 900,"start_y": 250,"iterations": 10,"direction": "increment","amount": 30},
            {"start_x": 1800,"start_y": 350,"iterations": 10,"direction": "increment","amount": 30},
            {"start_x": 2700,"start_y": 350,"iterations": 10,"direction": "increment","amount": 30},
        ],
        "spikes": [
            {"start_x": 800,"start_y": 350,"iterations": 3,"direction": "increment","amount": 400},
            {"start_x": 2500,"start_y": 350,"iterations": 1,"direction": "increment","amount": 100},
        ],
        "home": {"start_x": 3000,"start_y": 180,"width": 250,"height": 250},
    },
    {
        "tiles": [
            {
                "type": "3",
                "start_x": 0,
                "start_y": 400,
                "iterations": 50,
                "direction": "increment",
                "amount": 50
            },
            {
                "type": "18",
                "start_x": 0,
                "start_y": 450,
                "iterations": 50,
                "direction": "increment",
                "amount": 50
            },
            # ... other tile configurations
        ],
        "coins": [
            {
                "start_x": 50,
                "start_y": 350,
                "iterations": 10,
                "direction": "increment",
                "amount": 30
            },
            # ... other coin configurations
        ],
        "spikes": [
            {
                "start_x": 1000,
                "start_y": 350,
                "iterations": 5,
                "direction": "increment",
                "amount": 400
            },
        ],
        "home": {
            "start_x": 2000,
            "start_y": 180,
            "width": 250,
            "height": 250
        }
    }
]