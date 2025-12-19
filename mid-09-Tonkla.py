{
  "cells": [
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "view-in-github",
        "colab_type": "text"
      },
      "source": [
        "<a href=\"https://colab.research.google.com/github/Tonkla789/09-coding68/blob/main/mid-09-Tonkla.py\" target=\"_parent\"><img src=\"https://colab.research.google.com/assets/colab-badge.svg\" alt=\"Open In Colab\"/></a>"
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "score = float(input(\"\\nกรอกค่า confidence score 0.0-1.0:\"))\n",
        "print(\"แสดงผล\")\n",
        "if score >= 0.8:\n",
        "  print(\"High Confidence\")\n",
        "else:\n",
        " print(\"Low Confidence\")"
      ],
      "metadata": {
        "id": "5aeDafi5wGoh",
        "outputId": "3bb575e0-fcd5-4d8c-9add-00e968290af7",
        "colab": {
          "base_uri": "https://localhost:8080/"
        }
      },
      "execution_count": 2,
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "\n",
            "กรอกค่า confidence score 0.0-1.0:0.5\n",
            "แสดงผล\n",
            "Low Confidence\n"
          ]
        }
      ]
    }
  ],
  "metadata": {
    "colab": {
      "name": "ยินดีต้อนรับสู่ Colab",
      "toc_visible": true,
      "provenance": [],
      "include_colab_link": true
    },
    "kernelspec": {
      "display_name": "Python 3",
      "name": "python3"
    }
  },
  "nbformat": 4,
  "nbformat_minor": 0
}