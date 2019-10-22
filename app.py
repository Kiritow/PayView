# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import time


if __name__ == "__main__":
    with open("total.csv", encoding="utf-8") as f:
        content = f.read()

    title_cn_lst = "交易时间,交易类型,交易对方,商品,收/支,金额(元),支付方式,当前状态,交易单号,商户单号,备注".split(',')
    title_lst = "f_trade_time,f_trade_type,f_trade_with,f_trade_item,f_cash_flow,f_amount,f_pay_type,f_trade_status,f_trade_id,f_pos_id,f_comment".split(',')

    result = []

    for line in content.replace('\r', '').split('\n'):
        tmp = line.split(',')
        if len(tmp) != len(title_lst):
            continue
        data = {}
        for i in range(len(title_lst)):
            if title_lst[i] == "f_amount":
                data[title_lst[i]] = float(tmp[i].strip()[1:])
            else:
                data[title_lst[i]] = tmp[i].strip()
        result.append(data)

    income_total = 0
    outgo_total = 0

    for row in result:
        print(row)
        if row['f_cash_flow'] == "收入":
            income_total += row['f_amount']
        elif row['f_cash_flow'] == "支出":
            outgo_total += row['f_amount']
        elif row['f_cash_flow'] in ['/']:
            continue
        else:
            raise Exception("Unknown cash flow: {}".format(row['f_cash_flow']))

    print("总收入: {} 总支出: {}".format(income_total, outgo_total))

    def process_data(flow_type):
        graph_data = []

        for row in result:
            if row['f_cash_flow'] == flow_type:
                graph_data.append(row)

        graph_data = sorted(graph_data, key=lambda x: x['f_trade_time'])
        merged_data = {}
        x_data = []
        y_data = []

        for row in graph_data:
            offed_trade_timestamp = time.mktime(time.strptime(row['f_trade_time'].split(' ')[0] + " 00:00:00", "%Y-%m-%d %H:%M:%S"))
            begin_timestamp = time.mktime(time.strptime("2019-01-01 00:00:00", "%Y-%m-%d %H:%M:%S"))
            # 同一天的归到一起
            key = int(offed_trade_timestamp - begin_timestamp) / 3600 / 24
            if key not in merged_data:
                merged_data[key] = 0
            merged_data[key] += row['f_amount']

        for off_day in merged_data:
            x_data.append(off_day)
            y_data.append(merged_data[off_day])

        return x_data, y_data

    x_data, y_data = process_data("收入")
    plt.plot(x_data, y_data, label="Income")

    # for x, y in zip(x_data, y_data):
    #     plt.text(x, y, int(y), ha="center", va="bottom", fontsize=10)

    x_data, y_data = process_data("支出")
    plt.plot(x_data, y_data, label="Outgo")

    # for x, y in zip(x_data, y_data):
    #     plt.text(x, y, int(y), ha="center", va="bottom", fontsize=10)

    plt.legend()
    plt.show()
