{
  "nbformat": 4,
  "nbformat_minor": 0,
  "metadata": {
    "colab": {
      "provenance": [],
      "authorship_tag": "ABX9TyM8orJJvFxrSmijZHyDEbri",
      "include_colab_link": true
    },
    "kernelspec": {
      "name": "python3",
      "display_name": "Python 3"
    },
    "language_info": {
      "name": "python"
    }
  },
  "cells": [
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "view-in-github",
        "colab_type": "text"
      },
      "source": [
        "<a href=\"https://colab.research.google.com/github/Gayathri-rfr/DataPOC/blob/main/database.py\" target=\"_parent\"><img src=\"https://colab.research.google.com/assets/colab-badge.svg\" alt=\"Open In Colab\"/></a>"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": null,
      "metadata": {
        "id": "kg0RIlDWRc2W"
      },
      "outputs": [],
      "source": [
        "import sqlite3\n",
        "import pandas as pd\n",
        "import os\n",
        "\n",
        "DB_NAME = \"django_mock.db\"\n",
        "\n",
        "def init_db():\n",
        "    \"\"\"Initializes the database table if it doesn't exist.\"\"\"\n",
        "    conn = sqlite3.connect(DB_NAME)\n",
        "    cursor = conn.cursor()\n",
        "    cursor.execute('''\n",
        "        CREATE TABLE IF NOT EXISTS transaction_record (\n",
        "            id INTEGER PRIMARY KEY AUTOINCREMENT,\n",
        "            tx_id TEXT UNIQUE,\n",
        "            user_id INTEGER,\n",
        "            amount REAL,\n",
        "            category TEXT,\n",
        "            is_anomaly INTEGER\n",
        "        )\n",
        "    ''')\n",
        "    conn.commit()\n",
        "    conn.close()\n",
        "\n",
        "def save_to_django_db(data: dict) -> bool:\n",
        "    \"\"\"Simulates Django ORM's Model.objects.create()\"\"\"\n",
        "    conn = sqlite3.connect(DB_NAME)\n",
        "    cursor = conn.cursor()\n",
        "    try:\n",
        "        cursor.execute('''\n",
        "            INSERT INTO transaction_record (tx_id, user_id, amount, category, is_anomaly)\n",
        "            VALUES (?, ?, ?, ?, ?)\n",
        "        ''', (data['tx_id'], data['user_id'], data['amount'], data['category'], int(data['is_anomaly'])))\n",
        "        conn.commit()\n",
        "        success = True\n",
        "    except sqlite3.IntegrityError:\n",
        "        success = False  # Handles duplicate tx_id values gracefully\n",
        "    finally:\n",
        "        conn.close()\n",
        "    return success\n",
        "\n",
        "def get_django_records() -> list:\n",
        "    \"\"\"Simulates Django ORM's Model.objects.all().values()\"\"\"\n",
        "    if not os.path.exists(DB_NAME):\n",
        "        return []\n",
        "    conn = sqlite3.connect(DB_NAME)\n",
        "    df = pd.read_sql_query(\"SELECT * FROM transaction_record\", conn)\n",
        "    conn.close()\n",
        "    return df.to_dict(orient=\"records\")"
      ]
    }
  ]
}