def dash_list(input_list, list_sort, dep_dict, kpi):
    for item in input_list:
        if item.r_value:
            list_sort[item.month.strftime('%Y/%m/%d')] = item.r_value
        else:
            list_sort[item.month.strftime('%Y/%m/%d')] = 'NA'
        dep_dict[kpi] = {"t_value": item.group_kpi.t_value,
                         "l_limit": item.group_kpi.l_limit,
                         "r_value": dict(list_sort.items())}