import streamlit as st
import plotly.express as px
import json
import pathlib



def get_results(path, label):
    dir_path = pathlib.Path(path)

    data = []

    m16_files = [file for file in dir_path.glob("*m-16-*")]
    for file in m16_files:
        if "upload" in file.as_posix():
            continue
        with open(file, "r") as f:
            res = json.load(f)
            results = res["results"]
            ef = res["params"]["params"]["ef"]
            data.append(
                {
                    "db": "milvus",
                    "dataset": "gist-960-euclidean",
                    # "m": 16,
                    # "efc": 256,
                    # "ef": ef,
                    "label": label,
                    "group_label": f"milvus-{label}",
                    "name": f"milvus-m-16-efc-256-ef-{ef}-{label}",
                    "parallel": res["params"]["parallel"],
                    "recall": results["mean_precisions"],
                    "rps": results["rps"],
                }
            )

    m32_files = [file for file in dir_path.glob("*m-32-*")]
    for file in m32_files:
        if "upload" in file.as_posix():
            continue
        with open(file, "r") as f:
            res = json.load(f)
            results = res["results"]
            ef = res["params"]["params"]["ef"]
            data.append(
                {
                    "db": "milvus",
                    "dataset": "gist-960-euclidean",
                    # "m": 32,
                    # "efc": 256,
                    # "ef": ef,
                    "label": label,
                    "group_label": f"milvus-{label}",
                    "name": f"milvus-m-32-efc-256-ef-{ef}-{label}",
                    "parallel": res["params"]["parallel"],
                    "recall": results["mean_precisions"],
                    "rps": results["rps"],
                }
            )

    return data


def get_outdated_result(path):
    with open(path, "r") as f:
        res = json.load(f)
        gist_data = [d for d in res if d["dataset_name"] == "deep-image-96-angular"]
        label = "outdated"
        data = [
            {
                "db": d["engine_name"],
                "dataset": d["dataset_name"],
                "label": label,
                "group_label": f'{d["engine_name"]}-{label}',
                "name": f'{d["setup_name"]}-{label}',
                "parallel": d["parallel"],
                "recall": d["mean_precisions"],
                "rps": d["rps"]
            }
            for d in gist_data
        ]

        return data


def draw_charts(data):
    x = "recall"
    y = "rps"
    data.sort(key=lambda a: a[x])
    
    fig = px.line(
        data,
        x=x,
        y=y,
        color="group_label",
        line_group="group_label",
        # text="name",
        markers=True,
        hover_data={
            "group_label": False,
            "name": True,
            "db": False,
        },
    )
    # fig.update_xaxes(range=xrange)
    # fig.update_yaxes(range=yrange)
    # fig.update_traces(textposition="bottom right", texttemplate="%{y:,.4~r}")
    fig.update_layout(
        margin=dict(l=0, r=0, t=40, b=0, pad=8),
        legend=dict(
            orientation="h", yanchor="bottom", y=1, xanchor="right", x=1, title=""
        ),
    )
    st.plotly_chart(fig, use_container_width=True)


def main():
    compact_data = get_results("results-compact-m-16-32", "compact")
    no_compat_data = get_results("results-no-compact-m-16-32", "no-compact")
    outdated_data = get_outdated_result("results_from_qdrant.json")
    data = [*compact_data, *no_compat_data, *outdated_data]
    
    for parallel in [1, 2, 4, 8]:
        st.subheader(f"Parallel - {parallel}")
        draw_charts([d for d in data if d["parallel"] == parallel])
    


if __name__ == "__main__":
    main()
