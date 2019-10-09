import os
from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from bson.objectid import ObjectId

host = os.environ.get('MONGODB_URI', 'mongodb://localhost:27017/Contractor')
# host = MongoClient(host=f'{host}?retryWrites=false')
client = MongoClient(host=f'{host}?retryWrites=false')
db = client.get_default_database()
ridepasses = db.ridepasses
comments = db.comments

app = Flask(__name__)

@app.route('/')
def ridepasses_index():
    """Show available ridepasses."""
    return render_template('ridepasses_index.html', ridepasses=ridepasses.find())

@app.route('/ridepasses/new')
def ridepasses_new():
    """Create new ridepass."""
    return render_template('ridepasses_new.html', ridepass={}, title='New Ridepass')

@app.route('/ridepass', methods=['POST'])
def ridepasses_submit():
    """Submit a new ridepass."""
    ridepass = {
        'title': request.form.get('title'),
        'description': request.form.get('description'),
        'videos': request.form.get('videos').split()
    }
    ridepass_id = ridepasses.insert_one(ridepass).inserted_id
    return redirect(url_for('ridepasses_show', ridepass_id=ridepass_id))

@app.route('/ridepass/<ridepass_id>')
def ridepasses_show(ridepass_id):
    """Show a single ridepass."""
    ridepass = ridepasses.find_one({'_id': ObjectId(ridepass_id)})
    ridepass_comments = comments.find({'ridepass_id': ObjectId(ridepass_id)})
    return render_template('ridepasses_show.html', ridepass=ridepass, comments=ridepass_comments)

@app.route('/ridepasses/<ridepass_id>/edit')
def ridepasses_edit(ridepass_id):
    """Show the Edit form for a ridepass."""
    ridepass = ridepasses.find_one({'_id': ObjectId(ridepass_id)})
    return render_template('ridepasses_edit.html', ridepass=ridepass, title='Edit Ridepass')
    # return f'My ID is {playlist_id}'

@app.route('/ridepasses', methods=['POST'])
def ridepassess_update(ridepass_id):
    """Submit an edited ridepass."""
    updated_ridepass = {
        'title': request.form.get('title'),
        'description': request.form.get('description'),
        'videos': request.form.get('videos').split()
    }
    ridepassess.update_one(
        {'_id': ObjectId(ridepass_id)},
        {'$set': updated_ridepass})
    return redirect(url_for('ridepasses_show', ridepass_id=ridepass_id))

@app.route('/ridepasses/<ridepass_id>/delete', methods=['POST'])
def ridepasses_delete(ridepass_id):
    """Delete One ridepass."""
    ridepasses.delete_one({'_id': ObjectId(ridepass_id)})
    return redirect(url_for('ridepasses_index'))

@app.route('/ridepasses/comments', methods=['POST'])
def comments_new():
    """Submit a new comment."""
    comment = {
        'title': request.form.get('title'),
        'content': request.form.get('content'),
        'ridepass_id': ObjectId(request.form.get('ridepass_id'))
    }
    print(comment)
    comment_id = comments.insert_one(comment).inserted_id
    return redirect(url_for('ridepasses_show', ridepass_id=request.form.get('ridepass_id')))

@app.route('/ridepasses/comments/<comment_id>', methods=['POST'])
def comments_delete(comment_id):
    """Action to delete a comment."""
    comment = comments.find_one({'_id': ObjectId(comment_id)})
    comments.delete_one({'_id': ObjectId(comment_id)})
    return redirect(url_for('ridepasses_show', ridepass_id=comment.get('ridepass_id')))


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=os.environ.get('PORT', 5000))
