recommendation_map = {
    "Alluvial": {
        "Crops": "Wheat, Rice, Sugarcane",
        "Fertilizer": "Nitrogen-rich fertilizer",
        "Irrigation": "Weekly irrigation recommended"
    },
    "Black": {
        "Crops": "Cotton, Soybean, Millets",
        "Fertilizer": "Phosphorus-rich fertilizer",
        "Irrigation": "Retains moisture well, irrigate biweekly"
    },
    "Red": {
        "Crops": "Groundnut, Sorghum",
        "Fertilizer": "Organic manure or compost",
        "Irrigation": "Frequent irrigation required"
    },
    "Laterite": {
        "Crops": "Tea, Coffee, Cashew",
        "Fertilizer": "Potash and phosphate-based fertilizers",
        "Irrigation": "Moderate irrigation"
    },
    "Sandy": {
        "Crops": "Melons, Peanuts, Potatoes",
        "Fertilizer": "Slow-release nitrogen",
        "Irrigation": "Frequent, light irrigation"
    }
}

def get_recommendation(soil_type):
    return recommendation_map.get(soil_type, {
        "Crops": "N/A",
        "Fertilizer": "N/A",
        "Irrigation": "N/A"
    })
