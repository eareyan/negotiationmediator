def get_bounds(the_scenario):
    # Compute the bounds of the utility functions from the XML file
    bounds = []
    for i in the_scenario.getroot()[0]:
        bounds += ((float(i.attrib['lowerbound']), float(i.attrib['upperbound'])),)
    return bounds


def get_value_max_hyperrect(agents_u_fun):
    return max([d['height'] for a, h in agents_u_fun.items() for d in h])


def get_value_sum_hyperrect(agents_u_fun):
    return sum([d['height'] for a, h in agents_u_fun.items() for d in h])


def read_ufuns(the_scenario):
    root = the_scenario.getroot()
    agents_u_fun = {}
    a = 0
    # all items data
    for elem in root:
        if elem.tag == 'profile':
            if len(elem) != 1 or elem[0].tag != 'ufun':
                raise Exception("Each agent must have a unique ufun")
            ufun = []
            for cube in elem[0]:
                b_map = {'height': float(cube.attrib['height'])}
                for b in cube:
                    b_map['issue_' + b.attrib['issue']] = {'min': float(b.attrib['min']), 'max': float(b.attrib['max'])}
                ufun += [b_map]
            agents_u_fun[a] = ufun
            a += 1
    return agents_u_fun


def get_agent_u(a, the_xml_u_funcs):
    def u(x):
        return query_ufun(x, a, the_xml_u_funcs)

    return u


def get_ufuns(the_scenario):
    return {a: get_agent_u(a, read_ufuns(the_scenario)) for a in range(0, 2)}


def query_ufun(the_contract, the_agent, the_agents_u_fun):
    the_total_value = 0.0
    for h in the_agents_u_fun[the_agent]:
        consider_h = True
        for i in range(0, len(the_contract)):
            issue = 'issue_' + str(i + 1)
            if issue in h:
                # print('Check issue: ', str(i + 1), '\t min = ', h[issue]['min'], '\tmax = ', h[issue]['max'],
                #      '\t height =', h['height'])
                if h[issue]['min'] > the_contract[i] or h[issue]['max'] < the_contract[i]:
                    # print('\t Not Valid')
                    consider_h = False
                    break
        if consider_h:
            the_total_value += h['height']
            # print('\t We should consider ')
    return the_total_value
