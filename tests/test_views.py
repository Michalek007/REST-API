#
# def test_install_software_in_progress(client):
#     request_software_id = 0
#     write_example_file(request_software_id, 'InProgress')
#     with app.app_context():
#         url = url_for('install_software',
#                       RequestSoftwareID=request_software_id,
#                       SoftwareName='test',
#                       SoftwareVersion='test')
#     response = client.get(url).json
#     client.get('/clear_status_logs/')
#     assert response['message'] == 'Software installation is already in progress.'
