from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st


# --------------------------------------------------
# Page configuration
# --------------------------------------------------

st.set_page_config(
    page_title="ACL Recovery Analytics",
    layout="wide"
)


# --------------------------------------------------
# Load processed dataset
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[1]

DATA_PATH = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "bilateral_semg_features.csv"
)


@st.cache_data
def load_data():
    return pd.read_csv(DATA_PATH)


df = load_data()


# --------------------------------------------------
# Shared datasets
# --------------------------------------------------

analysis_df = df[
    df["Primary_Analysis"] == True
].copy()

acl_df = analysis_df[
    analysis_df["Cohort"] == "ACL Patient"
].copy()

healthy_df = analysis_df[
    analysis_df["Cohort"] == "Healthy Control"
].copy()


# --------------------------------------------------
# Header
# --------------------------------------------------

st.title("ACL Recovery Analytics")

st.write(
    "Participant-level bilateral sEMG analytics prototype."
)

st.info(
    "Exploratory research prototype — not a clinical diagnostic "
    "or return-to-sport tool."
)


# --------------------------------------------------
# Navigation
# --------------------------------------------------

st.sidebar.header("Navigation")

page = st.sidebar.radio(
    "Select view",
    [
        "Cohort Overview",
        "Participant Explorer"
    ]
)


# ==================================================
# PAGE 1 — COHORT OVERVIEW
# ==================================================

if page == "Cohort Overview":

    st.subheader("Cohort Overview")

    st.write(
        "Summary of QC-valid ACL patients and healthy controls "
        "included in the primary analysis."
    )

    # --------------------------------------------------
    # Sample overview
    # --------------------------------------------------

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "ACL Participants",
            len(acl_df)
        )

    with col2:
        st.metric(
            "Healthy Controls",
            len(healthy_df)
        )

    with col3:
        st.metric(
            "Mean ACL Asymmetry",
            f"{acl_df['Symmetry_Deviation'].mean():.3f}"
        )

    with col4:
        st.metric(
            "Mean Healthy Asymmetry",
            f"{healthy_df['Symmetry_Deviation'].mean():.3f}"
        )


    # --------------------------------------------------
    # Main cohort finding
    # --------------------------------------------------

    st.markdown("### Cohort-Level Finding")

    mean_difference = (
        acl_df["Symmetry_Deviation"].mean()
        - healthy_df["Symmetry_Deviation"].mean()
    )

    st.write(
        f"The mean bilateral symmetry deviation was "
        f"**{acl_df['Symmetry_Deviation'].mean():.3f}** for ACL patients "
        f"and **{healthy_df['Symmetry_Deviation'].mean():.3f}** for healthy "
        f"controls, corresponding to an observed mean difference of "
        f"**{mean_difference:.3f}**."
    )

    st.write(
        "The group averages are very similar in this exploratory sample. "
        "However, participant-level analysis reveals substantial "
        "heterogeneity within the ACL cohort."
    )
    # --------------------------------------------------
    # Cohort distribution comparison
    # --------------------------------------------------

    st.markdown("### Cohort Distribution Comparison")

    st.write(
        "Participant-level symmetry deviation reveals the distribution "
        "behind the cohort averages."
    )

    fig, ax = plt.subplots(figsize=(9, 4))

    acl_values = (
        acl_df["Symmetry_Deviation"]
        .dropna()
    )

    healthy_values = (
        healthy_df["Symmetry_Deviation"]
        .dropna()
    )

    # Plot individual participants
    ax.scatter(
        healthy_values,
        [0] * len(healthy_values),
        label="Healthy controls",
        alpha=0.75,
        s=70
    )

    ax.scatter(
        acl_values,
        [1] * len(acl_values),
        label="ACL patients",
        alpha=0.75,
        s=70
    )

    # Add cohort medians
    ax.axvline(
        healthy_values.median(),
        linestyle="--",
        alpha=0.7,
        label="Healthy median"
    )

    ax.axvline(
        acl_values.median(),
        linestyle=":",
        alpha=0.7,
        label="ACL median"
    )

    ax.set_yticks([0, 1])
    ax.set_yticklabels(["Healthy Control", "ACL Patient"])

    ax.set_xlabel(
        "Symmetry Deviation |log(Involved / Uninvolved RMS)|"
    )

    ax.set_title(
        "Bilateral Asymmetry Distribution by Cohort"
    )

    ax.legend()

    plt.tight_layout()

    st.pyplot(fig)

    plt.close(fig)


    # --------------------------------------------------
    # Build review priority
    # --------------------------------------------------

    acl_screening = acl_df.copy()

    def assign_review_priority(score):

        if score > 2:
            return "High review priority"

        elif score > 1:
            return "Moderate review priority"

        else:
            return "Routine review"


    acl_screening["Review_Priority"] = (
        acl_screening[
            "Robust_Asymmetry_Score"
        ].apply(assign_review_priority)
    )


    # --------------------------------------------------
    # Review priority + direction summaries
    # --------------------------------------------------

    st.markdown("### ACL Screening Summary")

    summary_col1, summary_col2 = st.columns(2)


    with summary_col1:

        st.markdown("#### Review Priority")

        priority_counts = (
            acl_screening[
                "Review_Priority"
            ]
            .value_counts()
            .reindex(
                [
                    "High review priority",
                    "Moderate review priority",
                    "Routine review"
                ],
                fill_value=0
            )
        )

        st.dataframe(
            priority_counts
            .rename("Participants")
            .reset_index()
            .rename(
                columns={
                    "index": "Review Priority"
                }
            ),
            hide_index=True,
            use_container_width=True
        )


    with summary_col2:

        st.markdown("#### Activation Direction")

        direction_counts = (
            acl_screening[
                "Activation_Direction"
            ]
            .value_counts()
        )

        st.dataframe(
            direction_counts
            .rename("Participants")
            .reset_index()
            .rename(
                columns={
                    "index": "Activation Direction"
                }
            ),
            hide_index=True,
            use_container_width=True
        )


    # --------------------------------------------------
    # Cohort visualizations
    # --------------------------------------------------

    st.markdown("### Cohort Visual Analytics")

    plot_col1, plot_col2 = st.columns(2)


    # --------------------------------------------------
    # Plot 1 — Robust asymmetry
    # --------------------------------------------------

    with plot_col1:

        st.markdown(
            "#### Individual Asymmetry Relative to Healthy Reference"
        )

        plot_df = acl_screening.sort_values(
            "Robust_Asymmetry_Score",
            ascending=True
        )

        fig1, ax1 = plt.subplots(
            figsize=(7, 6)
        )

        y = range(len(plot_df))

        ax1.scatter(
            plot_df["Robust_Asymmetry_Score"],
            y,
            s=80
        )

        ax1.axvline(
            0,
            linestyle="--",
            label="Healthy median"
        )

        ax1.axvline(
            1,
            linestyle=":",
            label="Moderate review threshold"
        )

        ax1.axvline(
            2,
            linestyle=":",
            label="High review threshold"
        )

        ax1.set_yticks(
            list(y)
        )

        ax1.set_yticklabels(
            plot_df["Participant"]
        )

        ax1.set_xlabel(
            "Robust Asymmetry Score (MAD units)"
        )

        ax1.set_ylabel(
            "ACL Participant"
        )

        ax1.legend()

        st.pyplot(fig1)

        plt.close(fig1)


    # --------------------------------------------------
    # Plot 2 — RMS ratio
    # --------------------------------------------------

    with plot_col2:

        st.markdown(
            "#### Direction of Bilateral Activation"
        )

        ratio_df = acl_screening.sort_values(
            "RMS_Ratio",
            ascending=True
        )

        fig2, ax2 = plt.subplots(
            figsize=(7, 6)
        )

        y = range(len(ratio_df))

        ax2.scatter(
            ratio_df["RMS_Ratio"],
            y,
            s=80
        )

        ax2.axvline(
            1,
            linestyle="--",
            label="Equal bilateral activation"
        )

        ax2.axvspan(
            0.9,
            1.1,
            alpha=0.15,
            label="±10% exploratory symmetry band"
        )

        ax2.set_yticks(
            list(y)
        )

        ax2.set_yticklabels(
            ratio_df["Participant"]
        )

        ax2.set_xlabel(
            "Involved / Uninvolved Active RMS Ratio"
        )

        ax2.set_ylabel(
            "ACL Participant"
        )

        ax2.legend()

        st.pyplot(fig2)

        plt.close(fig2)


    # --------------------------------------------------
    # Flagged participants
    # --------------------------------------------------

    st.markdown(
        "### Participants Flagged for Additional Analytical Review"
    )

    flagged = acl_screening[
        acl_screening["Review_Priority"]
        != "Routine review"
    ].copy()

    st.dataframe(
        flagged[
            [
                "Participant",
                "RMS_Ratio",
                "Activation_Difference_Pct",
                "Activation_Direction",
                "Robust_Asymmetry_Score",
                "Review_Priority"
            ]
        ].round(3),
        hide_index=True,
        use_container_width=True
    )

    st.caption(
        "Review priority is an exploratory analytics label based on "
        "distance from the healthy reference distribution. It is not "
        "a clinical risk classification."
    )
    # --------------------------------------------------
    # Quick participant lookup
    # --------------------------------------------------

    st.markdown("### Quick Participant Lookup")

    quick_participant = st.selectbox(
        "Select a flagged participant for quick review",
        flagged["Participant"].tolist()
    )

    quick_row = flagged[
        flagged["Participant"] == quick_participant
    ].iloc[0]

    q1, q2, q3 = st.columns(3)

    with q1:
        st.metric(
            "RMS Ratio",
            f"{quick_row['RMS_Ratio']:.3f}"
        )

    with q2:
        st.metric(
            "Activation Difference",
            f"{quick_row['Activation_Difference_Pct']:.1f}%"
        )

    with q3:
        st.metric(
            "Asymmetry Score",
            f"{quick_row['Robust_Asymmetry_Score']:.2f}"
        )

    st.write(
        f"**Activation pattern:** "
        f"{quick_row['Activation_Direction']}"
    )

    st.write(
        f"**Review priority:** "
        f"{quick_row['Review_Priority']}"
    )

# ==================================================
# PAGE 2 — PARTICIPANT EXPLORER
# ==================================================
elif page == "Participant Explorer":

    # --------------------------------------------------
    # Participant selector
    # --------------------------------------------------

    st.sidebar.divider()

    st.sidebar.header(
        "Participant Selection"
    )

    participant_options = (
        df["Participant"]
        .tolist()
    )

    selected_participant = (
        st.sidebar.selectbox(
            "Select participant",
            participant_options
        )
    )


    participant = df[
        df["Participant"]
        == selected_participant
    ].iloc[0]


    # --------------------------------------------------
    # Participant header
    # --------------------------------------------------

    st.subheader(
        f"Participant Profile: "
        f"{selected_participant}"
    )

    st.caption(
        f"Cohort: {participant['Cohort']}"
    )


    # --------------------------------------------------
    # QC guardrail
    # --------------------------------------------------

    if not bool(
        participant["Primary_Analysis"]
    ):

        st.warning(
            "QC review required before "
            "generating a full assessment."
        )

        col1, col2 = st.columns(2)

        with col1:

            st.metric(
                "Involved-side QC",
                participant[
                    "Involved_QC_Status"
                ]
            )

        with col2:

            st.metric(
                "Uninvolved-side QC",
                participant[
                    "Uninvolved_QC_Status"
                ]
            )

        st.write(
            "This participant is not included "
            "in the primary analytical sample "
            "because at least one recording "
            "did not pass the predefined "
            "signal-quality criteria."
        )

        st.stop()


    # --------------------------------------------------
    # Key metrics
    # --------------------------------------------------

    col1, col2, col3, col4 = (
        st.columns(4)
    )

    with col1:

        st.metric(
            "RMS Ratio",
            f"{participant['RMS_Ratio']:.3f}"
        )

    with col2:

        st.metric(
            "Activation Difference",
            f"{participant['Activation_Difference_Pct']:.1f}%"
        )

    with col3:

        st.metric(
            "Asymmetry Score",
            f"{participant['Robust_Asymmetry_Score']:.2f}"
        )

    with col4:

        st.metric(
            "Reference Category",
            participant[
                "Asymmetry_Category"
            ]
        )


    # --------------------------------------------------
    # Activation pattern
    # --------------------------------------------------

    st.markdown(
        "### Activation Pattern"
    )

    st.write(
        f"**Direction:** "
        f"{participant['Activation_Direction']}"
    )

    st.write(
        f"Valid contractions: "
        f"{int(participant['Involved_Valid_Contractions'])} involved / "
        f"{int(participant['Uninvolved_Valid_Contractions'])} uninvolved"
    )
    # --------------------------------------------------
    # Automated analytical interpretation
    # --------------------------------------------------

    st.markdown("### Analytical Interpretation")

    score = participant["Robust_Asymmetry_Score"]
    direction = participant["Activation_Direction"]
    difference = participant["Activation_Difference_Pct"]

    if score > 2:
        review_priority = "High review priority"
        priority_text = (
            "This participant shows a relatively large deviation "
            "from the healthy reference distribution."
        )

    elif score > 1:
        review_priority = "Moderate review priority"
        priority_text = (
            "This participant shows a moderate deviation "
            "from the healthy reference distribution."
        )

    else:
        review_priority = "Routine review"
        priority_text = (
            "This participant falls relatively close "
            "to the healthy reference distribution."
        )

    if direction == "Involved side lower":
        direction_text = (
            f"The involved side shows approximately {difference:.1f}% "
            "lower activation than the uninvolved side."
        )

    elif direction == "Involved side higher":
        direction_text = (
            f"The involved side shows approximately {difference:.1f}% "
            "higher activation than the uninvolved side."
        )

    else:
        direction_text = (
            "Bilateral activation is approximately symmetric."
        )

    st.write(
        f"**Review priority:** {review_priority}"
    )

    st.write(direction_text)

    st.write(priority_text)

    st.caption(
        "Interpretation is based on exploratory bilateral sEMG metrics "
        "and the healthy reference distribution in this dataset. "
        "It should not be interpreted as a diagnosis, rehabilitation "
        "recommendation, or return-to-sport decision."
)
    # --------------------------------------------------
    # Visual analytics
    # --------------------------------------------------

    st.markdown(
        "### Visual Analytics"
    )

    plot_col1, plot_col2 = (
        st.columns(2)
    )


    # --------------------------------------------------
    # Bilateral activation
    # --------------------------------------------------

    with plot_col1:

        st.markdown(
            "#### Bilateral Muscle Activation"
        )

        fig1, ax1 = plt.subplots(
            figsize=(6, 4)
        )

        ax1.bar(
            [
                "Involved",
                "Uninvolved"
            ],
            [
                participant[
                    "Involved_RMS"
                ],
                participant[
                    "Uninvolved_RMS"
                ]
            ]
        )

        ax1.set_ylabel(
            "Mean Active RMS (V)"
        )

        ax1.set_title(
            f"{selected_participant}: "
            f"Active sEMG"
        )

        st.pyplot(fig1)

        plt.close(fig1)


    # --------------------------------------------------
    # Healthy reference comparison
    # --------------------------------------------------

    with plot_col2:

        st.markdown(
            "#### Relative to Healthy Reference"
        )

        healthy_values = (
            healthy_df[
                "Symmetry_Deviation"
            ]
            .dropna()
        )

        healthy_median = (
            healthy_values.median()
        )

        fig2, ax2 = plt.subplots(
            figsize=(6, 4)
        )

        ax2.scatter(
            healthy_values,
            [1] * len(
                healthy_values
            ),
            label="Healthy controls",
            alpha=0.7,
            s=70
        )

        ax2.scatter(
            participant[
                "Symmetry_Deviation"
            ],
            1,
            marker="*",
            s=220,
            label=selected_participant
        )

        ax2.axvline(
            healthy_median,
            linestyle="--",
            label="Healthy median"
        )

        ax2.set_xlabel(
            "Symmetry Deviation "
            "|log(Involved / Uninvolved RMS)|"
        )

        ax2.set_yticks([])

        ax2.set_title(
            "Asymmetry Relative "
            "to Healthy Reference"
        )

        ax2.legend()

        st.pyplot(fig2)

        plt.close(fig2)