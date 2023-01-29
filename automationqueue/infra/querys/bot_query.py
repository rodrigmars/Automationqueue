def capture_bot_query() -> str:

    return """INSERT INTO AUTOMATE_ENTROPY_DATA_CAPTURE(
        CODE,
        STATUS,
        PRICE,
        PRODUCT_MODEL) VALUES(
            :CODE,
            :STATUS,
            :PRICE,
            :PRODUCT_MODEL)"""

def intersection_bot_query() -> str:

    return """INSERT INTO AUTOMATE_ENTROPY_DATA_INTERSECTION(
        CODE,
        STATUS,
        PRICE,
        PRODUCT_MODEL) VALUES(
            :CODE,
            :STATUS,
            :PRICE,
            :PRODUCT_MODEL)"""
