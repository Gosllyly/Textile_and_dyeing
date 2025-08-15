import json
import os
import sys
from datetime import datetime
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from Machine_Distribution_lastest._GA_main import GA  # 从主模块导入GA类

def run_model(populationSize, crossoverRate, mutationRate, n_elite, iterationNumber, input_json_path, output_dir="results"):

    os.makedirs(output_dir, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    with open(input_json_path, 'r', encoding='gbk') as f:
        json_dict = json.load(f)

    model = GA(populationSize, crossoverRate, mutationRate, n_elite, iterationNumber, json_dict)

    result = model.main()
    output_path = os.path.join(output_dir, f"result_{timestamp}.json")
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    return f"result_{timestamp}.json"