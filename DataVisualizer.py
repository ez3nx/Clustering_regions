import plotly.graph_objects as go
import matplotlib.pyplot as plt

def plot_lines(title, labels, colors, mode_size, line_size, x_data, y_data):
    
    params_ = dict(
        showline=True,
        showgrid=False,
        showticklabels=True,
        linecolor='rgb(204, 204, 204)',
        linewidth=2,
        ticks='outside',
        tickfont=dict(
            family='Arial',
            size=12,
            color='rgb(82, 82, 82)',
        ),
    )
    
    fig = go.Figure()

    for i in range(len(labels)):
        dash_ = None
        if labels[i] == 'г. Москва':
            dash_ = 'dash'
        # lines
        fig.add_trace(go.Scatter(x=x_data[i], y=y_data[i], mode='lines',
            name=labels[i],
            line=dict(color=colors[i], width=line_size[i], dash=dash_),
            connectgaps=True,
        ))

        # endpoints
        fig.add_trace(go.Scatter(
            x=[x_data[i][0], x_data[i][-1]],
            y=[y_data[i][0], y_data[i][-1]],
            mode='markers',
            marker=dict(color=colors[i], size=mode_size[i])
        ))

    fig.update_layout(
        width=1000,
        height=600,
        xaxis=params_,
        yaxis=params_,
        autosize=False,
        margin=dict(
            autoexpand=False,
            l=80,
            r=100,
            t=110,
        ),
        showlegend=False,
        plot_bgcolor='white'
    )

    annotations = []

    # Adding labels
    for y_trace, label, color in zip(y_data, labels, colors):
        # labeling the left_side of the plot
        annotations.append(dict(xref='paper', x=0.05, y=y_trace[0],
                                    xanchor='right', yanchor='middle',
                                    text='',
                                    font=dict(family='Arial',
                                                size=16),
                                    showarrow=False))
        # labeling the right_side of the plot
        if label == 'Самарская область':
            _ = 0.05
        else:
            _ = 0
        annotations.append(dict(xref='paper', x=0.95, y=y_trace[12]+_,
                                    xanchor='left', yanchor='middle',
                                    text=f'{label}',
                                    font=dict(family='Arial',
                                                size=12),
                                    showarrow=False))
    # Title
    annotations.append(dict(xref='paper', yref='paper', x=0.0, y=1.05,
                                xanchor='left', yanchor='bottom',
                                text=title,
                                font=dict(family='Arial',
                                            size=24,
                                            color='rgb(37,37,37)'),
                                showarrow=False))
    # Source
    annotations.append(dict(xref='paper', yref='paper', x=0.5, y=-0.1,
                                xanchor='center', yanchor='top',
                                text='Росстат: https://rosstat.gov.ru/storage/mediabank/Innov-5.xls',
                                font=dict(family='Arial',
                                            size=12,
                                            color='rgb(150,150,150)'),
                                showarrow=False))

    fig.update_layout(annotations=annotations)
    fig.show()
    
def plot_elbow(inertia_, clr=None):
    
    plt.figure(figsize=(6,4))
    plt.title("The elbow method", fontsize=14)
    plt.scatter(x=[i for i in range(2,12)], y=inertia_, s=150, edgecolor='k', c=clr)
    plt.grid(True)
    plt.xlabel("Number of clusters", fontsize=12)
    plt.xticks([i for i in range(2,12)], fontsize=12)
    plt.ylabel("K-means score", fontsize=12)
    plt.tight_layout()
    plt.show()
    
def plot_silhouette(score_, clr=None):
    
    plt.figure(figsize=(6,4))
    plt.title("The silhouette coefficient method",fontsize=14)
    plt.scatter(x=[i for i in range(2,12)], y=score_, s=150, edgecolor='k', c=clr)
    plt.grid(True)
    plt.xlabel("Number of clusters", fontsize=12)
    plt.ylabel("Silhouette score", fontsize=12)
    plt.xticks([i for i in range(2,12)], fontsize=12)
    plt.yticks(fontsize=12)
    plt.tight_layout()
    plt.show()