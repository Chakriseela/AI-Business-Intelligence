import sqlite3
from pathlib import Path

from mcp.server.fastmcp import FastMCP


# ---------------------------------------------------------
# Paths
# ---------------------------------------------------------

# backend/mcp_server/server.py
# parents[2] -> project root: C:\HCLTECH\bizinsight-ai
PROJECT_ROOT = Path(__file__).resolve().parents[2]

DB_PATH = PROJECT_ROOT / "backend" / "database" / "business.db"


# ---------------------------------------------------------
# MCP Server
# ---------------------------------------------------------

mcp = FastMCP("BizInsight SQL Server")


# ---------------------------------------------------------
# SQL MCP Tool
# ---------------------------------------------------------

@mcp.tool()
def execute_readonly_sql(query: str) -> dict:
    """
    Execute a read-only SQL query against the BizInsight
    business database.

    Available tables:

    customers
        customer_id
        name
        email
        city
        customer_segment

    products
        product_id
        product_name
        category
        price
        cost
        stock_quantity

    orders
        order_id
        customer_id
        order_date
        status
        total_amount

    order_items
        order_item_id
        order_id
        product_id
        quantity
        unit_price

    Only SELECT queries are allowed.
    """

    query = query.strip()

    # Basic validation
    if not query:
        return {
            "success": False,
            "error": "Query cannot be empty."
        }

    # Only allow SELECT statements
    if not query.lower().startswith("select"):
        return {
            "success": False,
            "error": "Only SELECT queries are allowed."
        }

    # Block potentially dangerous SQL keywords
    blocked_keywords = [
        "insert ",
        "update ",
        "delete ",
        "drop ",
        "alter ",
        "create ",
        "replace ",
        "attach ",
        "detach ",
        "pragma ",
    ]

    query_lower = query.lower()

    for keyword in blocked_keywords:
        if keyword in query_lower:
            return {
                "success": False,
                "error": f"Blocked SQL operation: {keyword.strip()}"
            }

    if not DB_PATH.exists():
        return {
            "success": False,
            "error": f"Database not found: {DB_PATH}"
        }

    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row

        cursor = conn.cursor()

        cursor.execute(query)

        rows = cursor.fetchall()

        data = [dict(row) for row in rows]

        conn.close()

        return {
            "success": True,
            "row_count": len(data),
            "data": data
        }

    except sqlite3.Error as e:
        return {
            "success": False,
            "error": str(e)
        }


# ---------------------------------------------------------
# Run MCP Server
# ---------------------------------------------------------

if __name__ == "__main__":
    mcp.run()