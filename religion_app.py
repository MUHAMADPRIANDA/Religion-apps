import streamlit as st
import pandas as pd
import plotly.graph_objects as go

@st.cache_data
def load_data():
    df = pd.read_csv('WRP_global_data.csv')
    return df

# Load data
df = load_data()

# Sidebar 
st.sidebar.title('Pilih Tahun dan Agama')
years = df['year'].unique()
selected_year = st.sidebar.selectbox('Tahun', sorted(years))

religions = {
    'Protestant Christianity': 'chrstprot',
    'Catholic Christianity': 'chrstcat',
    'Orthodox Christianity': 'chrstorth',
    'Anglican Christianity': 'chrstang',
    'Other Christianity': 'chrstothr',
    'Total Christianity': 'chrstgen',
    'Orthodox Judaism': 'judorth',
    'Conservative Judaism': 'jdcons',
    'Reform Judaism': 'judref',
    'Other Judaism': 'judothr',
    'Total Judaism': 'judgen',
    'Sunni Islam': 'islmsun',
    'Shi\'a Islam': 'islmshi',
    'Ibadi Islam': 'islmibd',
    'Nation of Islam': 'islmnat',
    'Alawite Islam': 'islmalw',
    'Ahmadiyya Islam': 'islmahm',
    'Other Islam': 'islmothr',
    'Total Islam': 'islmgen',
    'Mahayana Buddhism': 'budmah',
    'Theravada Buddhism': 'budthr',
    'Other Buddhism': 'budothr',
    'Total Buddhism': 'budgen',
    'Zoroastrianism': 'zorogen',
    'Hinduism': 'hindgen',
    'Sikhism': 'sikhgen'
}

selected_religion = st.sidebar.selectbox('Agama', list(religions.keys()))
selected_religion_column = religions[selected_religion]

# Filter data berdasarkan tahun yang dipilih
filtered_df = df[df['year'] == selected_year]

# Plot time series jumlah pemeluk agama yang dipilih
fig1 = go.Figure()

fig1.add_trace(go.Scatter(
    x=df['year'],
    y=df[selected_religion_column],
    mode='lines',
    line=dict(color='royalblue', width=3)
))

# Menambahkan animasi untuk time series
frames = [go.Frame(data=[go.Scatter(x=df['year'][:k+1], y=df[selected_religion_column][:k+1], mode='lines', line=dict(color='royalblue', width=3))]) for k in range(len(df))]
fig1.update(frames=frames)
fig1.update_layout(
    title=f'Tren Jumlah Pemeluk {selected_religion} dari Waktu ke Waktu',
    xaxis=dict(title='Tahun'),
    yaxis=dict(title='Jumlah Pemeluk'),
    updatemenus=[
        dict(
            type='buttons',
            showactive=False,
            buttons=[
                dict(
                    label='Play',
                    method='animate',
                    args=[
                        None,
                        dict(
                            frame=dict(duration=100, redraw=True),
                            fromcurrent=True,
                            mode='immediate'
                        )
                    ]
                )
            ],
            x=0.95,  # Posisi tombol Play di tengah-tengah horizontal
            y=1.25,  # Posisi tombol Play di atas plot
            xanchor='right',
            yanchor='top'
        )
    ]
)

# Tampilkan plot time series 
st.title('Visualisasi Jumlah Pemeluk Agama berdasarkan Tahun')
st.plotly_chart(fig1)

# Mengubah data menjadi format panjang untuk plot bar chart
melted_df = filtered_df.melt(id_vars=['year'], value_vars=[religions[rel] for rel in religions.keys()],
                             var_name='Agama', value_name='Jumlah Pemeluk')

# Membersihkan koma (',') dari string angka dan konversi ke float
melted_df['Jumlah Pemeluk'] = melted_df['Jumlah Pemeluk'].str.replace(',', '').astype(float)

# Membuat bar chart dengan animasi intro menggunakan bar data yang ada
def create_bar_chart(data, title):
    fig = go.Figure()

    fig.add_trace(go.Bar(x=data['Agama'], y=data['Jumlah Pemeluk'], name="Data", width=0.5))  # Lebar bar diperbesar

    fig.update_layout(
        title=title,
        xaxis=dict(title='Agama', type='category'),
        yaxis=dict(title='Jumlah Pemeluk', type='linear'),
        showlegend=False
    )

    # Animasi intro 
    frames = [go.Frame(data=[go.Bar(x=data['Agama'], y=[i/100 * val for val in data['Jumlah Pemeluk']], width=0.5)]) for i in range(0, 101, 5)]  # Mengurangi jumlah frame
    fig.update(frames=frames)
    fig.update_layout(
        updatemenus=[
            dict(
                type="buttons",
                showactive=False,
                buttons=[
                    dict(label="Play",
                         method="animate",
                         args=[None, {"frame": {"duration": 30, "redraw": True}, "fromcurrent": True, "transition": {"duration": 0}}])  # Mengurangi durasi frame
                ],
                x=0.95,  # Posisi tombol Play di kanan horizontal
                y=1.25,  # Posisi tombol Play di atas plot
                xanchor='right',
                yanchor='top'
            )
        ]
    )

    return fig

fig2 = create_bar_chart(melted_df, f'Distribusi Pemeluk Agama pada Tahun {selected_year}')

# Menampilkan bar chart
st.plotly_chart(fig2)

# Tampilkan tabel data
st.title('Data Pemeluk Agama')
st.dataframe(filtered_df)
