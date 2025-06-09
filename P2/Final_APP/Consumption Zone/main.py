# Import necessary libraries
import tempfile  # for creating temporary files for uploaded video
import numpy as np  # for numerical operations
import json  # for loading JSON data

import streamlit as st  # web app framework
from streamlit_image_coordinates import streamlit_image_coordinates  # get coordinates from image clicks
import cv2  # OpenCV for video processing
from ultralytics import YOLO  # YOLO model for object detection
from detection import create_colors_info, detect  # custom detection and color config logic

import torch  # PyTorch for deep learning
from torch.nn.modules.container import Sequential  # model container (used for safe serialization)
from ultralytics.nn.tasks import DetectionModel  # YOLO model architecture

# Import sentiment analysis logic
from vader_sentiment_analysis import analyze_sentiment

def main():
    # Streamlit page configuration
    st.set_page_config(page_title="AI Powered Web Application for Football Tactical Analysis", layout="wide", initial_sidebar_state="expanded")
    st.title("SoccerSense⚽")

    # Sidebar video selection
    st.sidebar.title("Video Settings")
    demo_selected = st.sidebar.radio(label="Select Demo Video", options=["Club", "National Team"], horizontal=True)

    # Sidebar for video upload
    st.sidebar.markdown('---')
    st.sidebar.subheader("Video Upload")
    input_vide_file = st.sidebar.file_uploader('Upload a video file', type=['mp4','mov', 'avi', 'm4v', 'asf'])

    # Path for demo videos
    demo_vid_paths = {
        "Club": './demo_vid_1.mp4',
        "National Team": './demo_vid_2.mp4'
    }

    # Pre-defined team info for demo
    demo_team_info = {
        "Club": {"team1_name":"France","team2_name":"Switzerland","team1_p_color":'#1E2530','team1_gk_color':'#F5FD15','team2_p_color':'#FBFCFA','team2_gk_color':'#B1FCC4'},
        "National Team": {"team1_name":"Chelsea","team2_name":"Manchester City","team1_p_color":'#29478A','team1_gk_color':'#DC6258','team2_p_color':'#90C8FF','team2_gk_color':'#BCC703'}
    }

    selected_team_info = demo_team_info[demo_selected]

    # Use temporary file to hold uploaded or demo video
    tempf = tempfile.NamedTemporaryFile(suffix='.mp4', delete=False)
    if not input_vide_file:
        tempf.name = demo_vid_paths[demo_selected]
        demo_vid = open(tempf.name, 'rb')
        demo_bytes = demo_vid.read()
        st.sidebar.text('Demo video')
        st.sidebar.video(demo_bytes)
    else:
        tempf.write(input_vide_file.read())
        demo_vid = open(tempf.name, 'rb')
        demo_bytes = demo_vid.read()
        st.sidebar.text('Input video')
        st.sidebar.video(demo_bytes)

    # Load player and field keypoint detection models
    model_players = YOLO("../models/Yolo8L Players/weights/best.pt")
    model_keypoints = YOLO("../models/Yolo8M Field Keypoints/weights/best.pt")

    # Sidebar: team name input fields
    st.sidebar.markdown('---')
    st.sidebar.subheader("Team Names")
    team1_name = st.sidebar.text_input(label='First Team Name', value=selected_team_info["team1_name"])
    team2_name = st.sidebar.text_input(label='Second Team Name', value=selected_team_info["team2_name"])
    st.sidebar.markdown('---')

    # Main tab layout
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["Usage Instructions", "Teams Colors", "Video Detection", "Sentiment Analysis", "KPI Analytics"])

    # Tab 1: Instructions
    with tab1:
        st.header(':blue[Welcome!👋]')
        st.subheader('Primary Functions:', divider='blue')
        st.markdown("""
        ### 🏃‍♂️⚽ 1. Players and Ball Detection  
        Automatically detect and track players and the ball throughout the match.  
        Visualize positioning, movement, and team formations in real time.

        ### 💬📊 2. Match Comment Analysis  
        Upload and analyze fan comments to uncover sentiment and reactions.  
        Gain deeper insights into audience emotions during the match.

        ### 📈📚 3. Historical Data Analytics  
        Explore and compare past match and clubs statistics.  
        Use data to support strategy, scouting, and performance evaluation.
        """)

    

    with tab2:
        t1col1, t1col2 = st.columns([1,1])
        with t1col1:
            cap_temp = cv2.VideoCapture(tempf.name)
            frame_count = int(cap_temp.get(cv2.CAP_PROP_FRAME_COUNT))
            frame_nbr = st.slider(label="Select frame", min_value=1, max_value=frame_count, step=1, help="Select frame to pick team colors from")
            cap_temp.set(cv2.CAP_PROP_POS_FRAMES, frame_nbr)
            success, frame = cap_temp.read()
            with st.spinner('Detecting players in selected frame..'):
                results = model_players(frame, conf=0.7)
                bboxes = results[0].boxes.xyxy.cpu().numpy()
                labels = results[0].boxes.cls.cpu().numpy()
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                detections_imgs_list = []
                detections_imgs_grid = []
                padding_img = np.ones((80,60,3),dtype=np.uint8)*255
                for i, j in enumerate(list(labels)):
                    if int(j) == 0:
                        bbox = bboxes[i,:]                         
                        obj_img = frame_rgb[int(bbox[1]):int(bbox[3]), int(bbox[0]):int(bbox[2])]
                        obj_img = cv2.resize(obj_img, (60,80))
                        detections_imgs_list.append(obj_img)
                detections_imgs_grid.append([detections_imgs_list[i] for i in range(len(detections_imgs_list)//2)])
                detections_imgs_grid.append([detections_imgs_list[i] for i in range(len(detections_imgs_list)//2, len(detections_imgs_list))])
                if len(detections_imgs_list)%2 != 0:
                    detections_imgs_grid[0].append(padding_img)
                concat_det_imgs_row1 = cv2.hconcat(detections_imgs_grid[0])
                concat_det_imgs_row2 = cv2.hconcat(detections_imgs_grid[1])
                concat_det_imgs = cv2.vconcat([concat_det_imgs_row1,concat_det_imgs_row2])
            st.write("Detected players")
            value = streamlit_image_coordinates(concat_det_imgs, key="numpy")
            #value_radio_dic = defaultdict(lambda: None)
            st.markdown('---')
            radio_options =[f"{team1_name} P color", f"{team1_name} GK color",f"{team2_name} P color", f"{team2_name} GK color"]
            active_color = st.radio(label="Select which team color to pick from the image above", options=radio_options, horizontal=True,
                                    help="Chose team color you want to pick and click on the image above to pick the color. Colors will be displayed in boxes below.")
            if value is not None:
                picked_color = concat_det_imgs[value['y'], value['x'], :]
                st.session_state[f"{active_color}"] = '#%02x%02x%02x' % tuple(picked_color)
            st.write("Boxes below can be used to manually adjust selected colors.")
            cp1, cp2, cp3, cp4 = st.columns([1,1,1,1])
            with cp1:
                hex_color_1 = st.session_state[f"{team1_name} P color"] if f"{team1_name} P color" in st.session_state else selected_team_info["team1_p_color"]
                team1_p_color = st.color_picker(label=' ', value=hex_color_1, key='t1p')
                st.session_state[f"{team1_name} P color"] = team1_p_color
            with cp2:
                hex_color_2 = st.session_state[f"{team1_name} GK color"] if f"{team1_name} GK color" in st.session_state else selected_team_info["team1_gk_color"]
                team1_gk_color = st.color_picker(label=' ', value=hex_color_2, key='t1gk')
                st.session_state[f"{team1_name} GK color"] = team1_gk_color
            with cp3:
                hex_color_3 = st.session_state[f"{team2_name} P color"] if f"{team2_name} P color" in st.session_state else selected_team_info["team2_p_color"]
                team2_p_color = st.color_picker(label=' ', value=hex_color_3, key='t2p')
                st.session_state[f"{team2_name} P color"] = team2_p_color
            with cp4:
                hex_color_4 = st.session_state[f"{team2_name} GK color"] if f"{team2_name} GK color" in st.session_state else selected_team_info["team2_gk_color"]
                team2_gk_color = st.color_picker(label=' ', value=hex_color_4, key='t2gk')
                st.session_state[f"{team2_name} GK color"] = team2_gk_color
        st.markdown('---')


        
            

        with t1col2:
            extracted_frame = st.empty()
            extracted_frame.image(frame, use_column_width=True, channels="BGR")

        
    colors_dic, color_list_lab = create_colors_info(team1_name, st.session_state[f"{team1_name} P color"], st.session_state[f"{team1_name} GK color"],
                                                     team2_name, st.session_state[f"{team2_name} P color"], st.session_state[f"{team2_name} GK color"])


    with tab3:
        t2col1, t2col2 = st.columns([1,1])
        with t2col1:
            player_model_conf_thresh = st.slider('PLayers Detection Confidence Threshold', min_value=0.0, max_value=1.0, value=0.6)
            keypoints_model_conf_thresh = st.slider('Field Keypoints PLayers Detection Confidence Threshold', min_value=0.0, max_value=1.0, value=0.7)
            keypoints_displacement_mean_tol = st.slider('Keypoints Displacement RMSE Tolerance (pixels)', min_value=-1, max_value=100, value=7,
                                                         help="Indicates the maximum allowed average distance between the position of the field keypoints\
                                                           in current and previous detections. It is used to determine wether to update homography matrix or not. ")
            detection_hyper_params = {
                0: player_model_conf_thresh,
                1: keypoints_model_conf_thresh,
                2: keypoints_displacement_mean_tol
            }
        with t2col2:
            num_pal_colors = st.slider(label="Number of palette colors", min_value=1, max_value=5, step=1, value=3,
                                    help="How many colors to extract form detected players bounding-boxes? It is used for team prediction.")
            st.markdown("---")
            save_output = st.checkbox(label='Save output', value=False)
            if save_output:
                output_file_name = st.text_input(label='File Name (Optional)', placeholder='Enter output video file name.')
            else:
                output_file_name = None
        st.markdown("---")

        
        bcol1, bcol2 = st.columns([1,1])
        with bcol1:
            nbr_frames_no_ball_thresh = st.number_input("Ball track reset threshold (frames)", min_value=1, max_value=10000,
                                                     value=30, help="After how many frames with no ball detection, should the track be reset?")
            ball_track_dist_thresh = st.number_input("Ball track distance threshold (pixels)", min_value=1, max_value=1280,
                                                        value=100, help="Maximum allowed distance between two consecutive balls detection to keep the current track.")
            max_track_length = st.number_input("Maximum ball track length (Nbr. detections)", min_value=1, max_value=1000,
                                                        value=35, help="Maximum total number of ball detections to keep in tracking history")
            ball_track_hyperparams = {
                0: nbr_frames_no_ball_thresh,
                1: ball_track_dist_thresh,
                2: max_track_length
            }
        with bcol2:
            st.write("Annotation options:")
            bcol21t, bcol22t = st.columns([1,1])
            with bcol21t:
                show_k = st.toggle(label="Show Keypoints Detections", value=False)
                show_p = st.toggle(label="Show Players Detections", value=True)
            with bcol22t:
                show_pal = st.toggle(label="Show Color Palettes", value=True)
                show_b = st.toggle(label="Show Ball Tracks", value=True)
            plot_hyperparams = {
                0: show_k,
                1: show_pal,
                2: show_b,
                3: show_p
            }
            st.markdown('---')
            bcol21, bcol22, bcol23, bcol24 = st.columns([1.5,1,1,1])
            with bcol21:
                st.write('')
            with bcol22:
                ready = True if (team1_name == '') or (team2_name == '') else False
                start_detection = st.button(label='Start Detection', disabled=ready)
            with bcol23:
                stop_btn_state = True if not start_detection else False
                stop_detection = st.button(label='Stop Detection', disabled=stop_btn_state)
            with bcol24:
                st.write('')

    #with tab4:
    #    st.header("KPI Analytics")
    #    st.info("This section will display Key Performance Indicators (KPIs) and tactical insights extracted from the video analysis.")
    #    st.empty()
    import duckdb
    import io
    import pandas as pd
    import matplotlib.pyplot as plt



    with tab5:
        st.header("KPI Analytics")
        st.info("Upload related CSV files for KPI analysis and relational queries.")

        uploaded_files = st.file_uploader(
            label="Upload one or more related CSV files",
            type=["csv"],
            accept_multiple_files=True
        )

        if uploaded_files:
            st.success(f"{len(uploaded_files)} file(s) uploaded successfully.")

            # Create DuckDB connection
            con = duckdb.connect(database=':memory:')

            table_names = []

            for file in uploaded_files:
                table_name = file.name.replace(".csv", "").replace(" ", "_").lower()
                data = pd.read_csv(file)
                con.register(table_name, data)
                table_names.append(table_name)
                st.write(f"✅ Table `{table_name}` loaded")

            st.subheader("Preview of each table:")
            for table_name in table_names:
                st.write(f"**{table_name}**")
                df = con.execute(f"SELECT * FROM {table_name} LIMIT 5").df()
                st.dataframe(df)

            # 🧠 Derive KPI tables
            st.markdown("---")
            st.subheader("📊 KPI Visualizations")

            required_tables = {"appearances", "players", "club_games", "clubs"}
            if required_tables.issubset(set(table_names)):
                try:
                    # 1. player_performance
                    df_appearances = con.execute("SELECT * FROM appearances").df()
                    df_players = con.execute("SELECT * FROM players").df()

                    df_perf = df_appearances.groupby("player_id").agg({
                        "goals": "sum",
                        "assists": "sum",
                        "minutes_played": "mean"
                    })
                    df_perf["total_appearances"] = df_appearances.groupby("player_id").size()
                    df_perf = df_perf.rename(columns={
                        "goals": "total_goals",
                        "assists": "total_assists",
                        "minutes_played": "avg_minutes_played"
                    }).reset_index()
                    df_perf = df_perf.merge(df_players[["player_id", "name"]], on="player_id", how="left")

                    con.register("player_performance", df_perf)
                    table_names.append("player_performance")

                    # 2. club_performance
                    df_club_games = con.execute("SELECT * FROM club_games").df()
                    df_clubs = con.execute("SELECT * FROM clubs").df()

                    df_club_perf = df_club_games.copy()
                    df_club_perf["win"] = df_club_perf["is_win"].astype(int)
                    df_club_perf = df_club_perf.groupby("club_id").agg({
                        "win": "sum",
                        "club_id": "count"
                    }).rename(columns={"club_id": "total_games", "win": "wins"}).reset_index()
                    df_club_perf["win_rate"] = df_club_perf["wins"] / df_club_perf["total_games"]
                    df_club_perf = df_club_perf.merge(df_clubs[["club_id", "name"]], on="club_id", how="left")

                    con.register("club_performance", df_club_perf)
                    table_names.append("club_performance")

                    # 3. player_contribution
                    df_contrib = df_appearances.groupby("player_id").agg({
                        "goals": "sum",
                        "assists": "sum"
                    })
                    df_contrib["games"] = df_appearances.groupby("player_id").size()
                    df_contrib["contribution_rate"] = (df_contrib["goals"] + df_contrib["assists"]) / df_contrib["games"]
                    df_contrib = df_contrib.reset_index().merge(df_players[["player_id", "name"]], on="player_id", how="left")

                    con.register("player_contribution", df_contrib)
                    table_names.append("player_contribution")

                    st.success("Derived KPI tables created: player_performance, club_performance, player_contribution")

                    # 🎯 KPI Visualizations

                    # 1. Top Goal Scorers
                    st.markdown("### 🥅 Top 10 Goal Scorers")
                    top_scorers = df_perf.dropna(subset=["name"]).sort_values("total_goals", ascending=False).head(10)
                    fig1, ax1 = plt.subplots(figsize=(10, 5))
                    ax1.bar(top_scorers["name"], top_scorers["total_goals"])
                    ax1.set_title("Top 10 Goal Scorers")
                    ax1.set_xticklabels(top_scorers["name"], rotation=45, ha='right')
                    st.pyplot(fig1)

                    # 2. Top Clubs by Win Rate
                    st.markdown("### 🏆 Top 10 Clubs by Win Rate")
                    top_clubs = df_club_perf.dropna(subset=["name"]).sort_values("win_rate", ascending=False).head(10)
                    fig2, ax2 = plt.subplots(figsize=(10, 5))
                    ax2.bar(top_clubs["name"], top_clubs["win_rate"])
                    ax2.set_title("Top 10 Clubs by Win Rate")
                    ax2.set_xticklabels(top_clubs["name"], rotation=45, ha='right')
                    st.pyplot(fig2)

                    # 3. Top Players by Contribution Rate
                    st.markdown("### 🎯 Top 10 Players by Goal Contribution Rate")
                    top_contrib = df_contrib.dropna(subset=["name"]).sort_values("contribution_rate", ascending=False).head(10)
                    fig3, ax3 = plt.subplots(figsize=(10, 5))
                    ax3.bar(top_contrib["name"], top_contrib["contribution_rate"])
                    ax3.set_title("Top 10 Players by Goal Contribution Rate")
                    ax3.set_xticklabels(top_contrib["name"], rotation=45, ha='right')
                    st.pyplot(fig3)

                except Exception as e:
                    st.error(f"Error during KPI calculation or plotting: {e}")
            else:
                st.warning("Please upload the required tables: appearances, players, club_games, and clubs")




    # Tab4: Sentiment Analysis with VADER
    with tab4:
        st.header("Sentiment Analysis (VADER)")
        uploaded_file = st.file_uploader("Upload a YouTube Comments JSON file", type=["json"])

        if uploaded_file:
            try:
                json_data = json.load(uploaded_file)

                if isinstance(json_data, list):
                    df_sentiment = analyze_sentiment(json_data)
                    st.success("Sentiment analysis completed!")
                    st.dataframe(df_sentiment)

                    # Optional: Show sentiment distribution
                    # Optional: Show sentiment distribution
                    st.subheader("Sentiment Distribution")

                    import matplotlib.pyplot as plt

                    # 用 df_sentiment（你之前处理情感分析的DataFrame）
                    sentiment_counts = df_sentiment['sentiment'].value_counts()
                    labels = sentiment_counts.index
                    sizes = sentiment_counts.values

                    fig, ax = plt.subplots()
                    ax.pie(
                        sizes,
                        labels=[f"{label} ({count})" for label, count in zip(labels, sizes)],
                        autopct="%1.1f%%",
                        startangle=90
                    )
                    ax.axis("equal")  # 让饼图是圆形
                    st.pyplot(fig)



                else:
                    st.error("Uploaded JSON file is not a list of comments. Please upload a correct format.")

            except Exception as e:
                st.error(f"Failed to process file: {e}")



            



    stframe = st.empty()
    cap = cv2.VideoCapture(tempf.name)
    status = False

    if start_detection and not stop_detection:
        st.toast(f'Detection Started!')
        status = detect(cap, stframe, output_file_name, save_output, model_players, model_keypoints,
                         detection_hyper_params, ball_track_hyperparams, plot_hyperparams,
                           num_pal_colors, colors_dic, color_list_lab)
    else:
        try:
            # Release the video capture object and close the display window
            cap.release()
        except:
            pass
    if status:
        st.toast(f'Detection Completed!')
        cap.release()


if __name__=='__main__':
    try:
        main()
    except SystemExit:
        pass