var SEED_DATA = [
  {
    "id": 1,
    "name": "NVIDIA H100 80GB PCIe",
    "category": "gpu",
    "region": "国际",
    "unit": "美元/张",
    "subcategory": "",
    "prices": [
      {
        "price_type": "云平台时租",
        "price_value": 3.28
      },
      {
        "price_type": "代理价",
        "price_value": 31418.54
      },
      {
        "price_type": "官方价",
        "price_value": 28021.12
      }
    ]
  },
  {
    "id": 2,
    "name": "NVIDIA H100 80GB SXM",
    "category": "gpu",
    "region": "国际",
    "unit": "美元/张",
    "subcategory": "",
    "prices": [
      {
        "price_type": "云平台时租",
        "price_value": 4.76
      },
      {
        "price_type": "代理价",
        "price_value": 36621.82
      },
      {
        "price_type": "官方价",
        "price_value": 32693.2
      }
    ]
  },
  {
    "id": 3,
    "name": "NVIDIA H200 141GB",
    "category": "gpu",
    "region": "国际",
    "unit": "美元/张",
    "subcategory": "",
    "prices": [
      {
        "price_type": "云平台时租",
        "price_value": 5.46
      },
      {
        "price_type": "代理价",
        "price_value": 46342.2
      },
      {
        "price_type": "官方价",
        "price_value": 40824.28
      }
    ]
  },
  {
    "id": 4,
    "name": "NVIDIA B300 服务器",
    "category": "gpu",
    "region": "国际",
    "unit": "美元/台",
    "subcategory": "",
    "prices": [
      {
        "price_type": "云平台月租",
        "price_value": 26027.18
      },
      {
        "price_type": "代理价",
        "price_value": 497153.96
      },
      {
        "price_type": "官方价",
        "price_value": 451532.72
      }
    ]
  },
  {
    "id": 5,
    "name": "NVIDIA H100 80GB PCIe (国内)",
    "category": "gpu",
    "region": "国内",
    "unit": "万元/张",
    "subcategory": "",
    "prices": [
      {
        "price_type": "代理价",
        "price_value": 25.53
      },
      {
        "price_type": "官方价",
        "price_value": 21.82
      },
      {
        "price_type": "第三方平台价",
        "price_value": 24.31
      }
    ]
  },
  {
    "id": 6,
    "name": "NVIDIA H100 80GB SXM (国内)",
    "category": "gpu",
    "region": "国内",
    "unit": "万元/张",
    "subcategory": "",
    "prices": [
      {
        "price_type": "代理价",
        "price_value": 27.81
      },
      {
        "price_type": "官方价",
        "price_value": 27.22
      },
      {
        "price_type": "第三方平台价",
        "price_value": 29.81
      }
    ]
  },
  {
    "id": 7,
    "name": "NVIDIA H200 141GB (国内)",
    "category": "gpu",
    "region": "国内",
    "unit": "万元/张",
    "subcategory": "",
    "prices": [
      {
        "price_type": "代理价",
        "price_value": 35.13
      },
      {
        "price_type": "官方价",
        "price_value": 32.83
      },
      {
        "price_type": "第三方平台价",
        "price_value": 37.04
      }
    ]
  },
  {
    "id": 8,
    "name": "NVIDIA B300 服务器 (国内)",
    "category": "gpu",
    "region": "国内",
    "unit": "万元/台",
    "subcategory": "",
    "prices": [
      {
        "price_type": "代理价",
        "price_value": 400.71
      },
      {
        "price_type": "官方价",
        "price_value": 336.21
      },
      {
        "price_type": "第三方平台价",
        "price_value": 386.61
      }
    ]
  },
  {
    "id": 9,
    "name": "OpenAI GPT-4o",
    "category": "llm_intl",
    "region": "国际",
    "unit": "美元/百万Token",
    "subcategory": "",
    "prices": [
      {
        "price_type": "代理价(Input)",
        "price_value": 3.03
      },
      {
        "price_type": "代理价(Output)",
        "price_value": 11.88
      },
      {
        "price_type": "官方价(Input)",
        "price_value": 2.41
      },
      {
        "price_type": "官方价(Output)",
        "price_value": 9.66
      }
    ]
  },
  {
    "id": 10,
    "name": "OpenAI GPT-4o-mini",
    "category": "llm_intl",
    "region": "国际",
    "unit": "美元/百万Token",
    "subcategory": "",
    "prices": [
      {
        "price_type": "官方价(Input)",
        "price_value": 0.13
      },
      {
        "price_type": "官方价(Output)",
        "price_value": 0.59
      }
    ]
  },
  {
    "id": 11,
    "name": "OpenAI o4-mini",
    "category": "llm_intl",
    "region": "国际",
    "unit": "美元/百万Token",
    "subcategory": "",
    "prices": [
      {
        "price_type": "官方价(Input)",
        "price_value": 1.29
      },
      {
        "price_type": "官方价(Output)",
        "price_value": 4.2
      }
    ]
  },
  {
    "id": 12,
    "name": "Anthropic Claude 3.5 Sonnet",
    "category": "llm_intl",
    "region": "国际",
    "unit": "美元/百万Token",
    "subcategory": "",
    "prices": [
      {
        "price_type": "官方价(Input)",
        "price_value": 3.33
      },
      {
        "price_type": "官方价(Output)",
        "price_value": 14.88
      }
    ]
  },
  {
    "id": 13,
    "name": "Anthropic Claude 3 Opus",
    "category": "llm_intl",
    "region": "国际",
    "unit": "美元/百万Token",
    "subcategory": "",
    "prices": [
      {
        "price_type": "官方价(Input)",
        "price_value": 14.45
      },
      {
        "price_type": "官方价(Output)",
        "price_value": 74.18
      }
    ]
  },
  {
    "id": 14,
    "name": "Google Gemini 2.5 Pro",
    "category": "llm_intl",
    "region": "国际",
    "unit": "美元/百万Token",
    "subcategory": "",
    "prices": [
      {
        "price_type": "官方价(Input)",
        "price_value": 1.39
      },
      {
        "price_type": "官方价(Output)",
        "price_value": 9.93
      }
    ]
  },
  {
    "id": 15,
    "name": "Google Gemini 2.5 Flash",
    "category": "llm_intl",
    "region": "国际",
    "unit": "美元/百万Token",
    "subcategory": "",
    "prices": [
      {
        "price_type": "官方价(Input)",
        "price_value": 0.15
      },
      {
        "price_type": "官方价(Output)",
        "price_value": 0.58
      }
    ]
  },
  {
    "id": 16,
    "name": "xAI Grok-3",
    "category": "llm_intl",
    "region": "国际",
    "unit": "美元/百万Token",
    "subcategory": "",
    "prices": [
      {
        "price_type": "官方价(Input)",
        "price_value": 4.38
      },
      {
        "price_type": "官方价(Output)",
        "price_value": 17.42
      }
    ]
  },
  {
    "id": 17,
    "name": "Meta Llama 4 (Together AI)",
    "category": "llm_intl",
    "region": "国际",
    "unit": "美元/百万Token",
    "subcategory": "",
    "prices": [
      {
        "price_type": "平台价(Input)",
        "price_value": 0.17
      },
      {
        "price_type": "平台价(Output)",
        "price_value": 0.8
      }
    ]
  },
  {
    "id": 18,
    "name": "Mistral Large 2",
    "category": "llm_intl",
    "region": "国际",
    "unit": "美元/百万Token",
    "subcategory": "",
    "prices": [
      {
        "price_type": "官方价(Input)",
        "price_value": 2.03
      },
      {
        "price_type": "官方价(Output)",
        "price_value": 6.01
      }
    ]
  },
  {
    "id": 19,
    "name": "DeepSeek-V3",
    "category": "llm_domestic",
    "region": "国内",
    "unit": "元/百万Token",
    "subcategory": "",
    "prices": [
      {
        "price_type": "官方价(Input)",
        "price_value": 1.11
      },
      {
        "price_type": "官方价(Output)",
        "price_value": 2.07
      }
    ]
  },
  {
    "id": 20,
    "name": "DeepSeek-R1",
    "category": "llm_domestic",
    "region": "国内",
    "unit": "元/百万Token",
    "subcategory": "",
    "prices": [
      {
        "price_type": "官方价(Input)",
        "price_value": 3.98
      },
      {
        "price_type": "官方价(Output)",
        "price_value": 14.18
      }
    ]
  },
  {
    "id": 21,
    "name": "阿里通义千问 Qwen3-Plus",
    "category": "llm_domestic",
    "region": "国内",
    "unit": "元/百万Token",
    "subcategory": "",
    "prices": [
      {
        "price_type": "官方价(Input)",
        "price_value": 0.89
      },
      {
        "price_type": "官方价(Output)",
        "price_value": 1.88
      }
    ]
  },
  {
    "id": 22,
    "name": "阿里通义千问 Qwen3-Max",
    "category": "llm_domestic",
    "region": "国内",
    "unit": "元/百万Token",
    "subcategory": "",
    "prices": [
      {
        "price_type": "官方价(Input)",
        "price_value": 0.51
      },
      {
        "price_type": "官方价(Output)",
        "price_value": 2.2
      }
    ]
  },
  {
    "id": 23,
    "name": "百度文心一言 4.0 Turbo",
    "category": "llm_domestic",
    "region": "国内",
    "unit": "元/百万Token",
    "subcategory": "",
    "prices": [
      {
        "price_type": "官方价(Input)",
        "price_value": 27.89
      },
      {
        "price_type": "官方价(Output)",
        "price_value": 100.11
      }
    ]
  },
  {
    "id": 24,
    "name": "字节豆包 Pro",
    "category": "llm_domestic",
    "region": "国内",
    "unit": "元/百万Token",
    "subcategory": "",
    "prices": [
      {
        "price_type": "官方价(Input)",
        "price_value": 0.81
      },
      {
        "price_type": "官方价(Output)",
        "price_value": 1.77
      }
    ]
  },
  {
    "id": 25,
    "name": "智谱 GLM-4 Plus",
    "category": "llm_domestic",
    "region": "国内",
    "unit": "元/百万Token",
    "subcategory": "",
    "prices": [
      {
        "price_type": "官方价(Input)",
        "price_value": 51.31
      },
      {
        "price_type": "官方价(Output)",
        "price_value": 96.9
      }
    ]
  },
  {
    "id": 26,
    "name": "月之暗面 Kimi",
    "category": "llm_domestic",
    "region": "国内",
    "unit": "元/百万Token",
    "subcategory": "",
    "prices": [
      {
        "price_type": "官方价(Input)",
        "price_value": 12.3
      },
      {
        "price_type": "官方价(Output)",
        "price_value": 55.24
      }
    ]
  },
  {
    "id": 27,
    "name": "讯飞星火 4.0",
    "category": "llm_domestic",
    "region": "国内",
    "unit": "元/百万Token",
    "subcategory": "",
    "prices": [
      {
        "price_type": "官方价(Input)",
        "price_value": 32.42
      },
      {
        "price_type": "官方价(Output)",
        "price_value": 96.31
      }
    ]
  },
  {
    "id": 28,
    "name": "MiniMax abab7",
    "category": "llm_domestic",
    "region": "国内",
    "unit": "元/百万Token",
    "subcategory": "",
    "prices": [
      {
        "price_type": "官方价(Input)",
        "price_value": 0.46
      },
      {
        "price_type": "官方价(Output)",
        "price_value": 1.03
      }
    ]
  },
  {
    "id": 29,
    "name": "零一万物 Yi-Large",
    "category": "llm_domestic",
    "region": "国内",
    "unit": "元/百万Token",
    "subcategory": "",
    "prices": [
      {
        "price_type": "官方价(Input)",
        "price_value": 9.16
      },
      {
        "price_type": "官方价(Output)",
        "price_value": 28.96
      }
    ]
  },
  {
    "id": 30,
    "name": "百川 Baichuan 4",
    "category": "llm_domestic",
    "region": "国内",
    "unit": "元/百万Token",
    "subcategory": "",
    "prices": [
      {
        "price_type": "官方价(Input)",
        "price_value": 20.12
      },
      {
        "price_type": "官方价(Output)",
        "price_value": 56.77
      }
    ]
  }
];
