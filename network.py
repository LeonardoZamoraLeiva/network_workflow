import network
import pandas as pd
from pyvis.network import Network


def network_visualization_func(file):
    print('{} will be representated as an network HTML file'.format(file))
    print(file)
    output_name = file[0:-4]
    net = Network(width='50%', height='600px', notebook=True)
    df = pd.read_csv(file,delimiter=',')
    print(df)
    sources = df['Source']
    targets = df['Target']
    weights = df['Weight']
    distance = df['Raw distance']
    #domains = df['Domains']
    edge_data = zip(sources, targets, weights,distance)
    for e in edge_data:
        src = e[0]
        dst = e[1]
        w = e[2]
        distance = e[3]
        net.add_node(src, src, title=src)
        net.add_node(dst, dst, title=dst)
        net.add_edge(src, dst, value=w)
        net.add_edge(src, dst, value=distance)
    neighbor_map = net.get_adj_list()
    for node in net.nodes:
        node['title'] += ' Neighbors:<br>' + '<br>'.join(neighbor_map[node['id']])
        node['value'] = len(neighbor_map[node['id']])

    net.show_buttons(filter_=True)
    net.show('{}.html'.format(output_name))
