#currency_converter


from db_config import get_connection

def get_conversion_rate(to_currency):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        query = """
            SELECT rate FROM currency_rates
            WHERE from_currency = 'INR' AND to_currency = %s
        """
        cursor.execute(query, (to_currency.upper(),))
        result = cursor.fetchone()
        conn.close()

        if result:
            return float(result[0])
        else:
            return None
    except Exception as e:
        print(f"[ERROR] Could not fetch conversion rate: {e}")
        return None
