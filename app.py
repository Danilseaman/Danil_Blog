from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'  # Настраиваем подключение базы данных
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Отключаем нерабочий модуль
db = SQLAlchemy(app)  # Создаем базу данных

# Создаем класс с колонками таблицы
class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Уникальный идентификатор
    title = db.Column(db.String(100), nullable=False)  # Заголовок статьи
    intro = db.Column(db.String(300), nullable=False)  # Вступительный текст
    text = db.Column(db.Text, nullable=False)  # Полный текст статьи
    date = db.Column(db.DateTime, default=datetime.utcnow)  # Время статьи

    def __repr__(self):
        return '<Article %r>' % self.id


@app.route('/')
@app.route('/home')
def index():
    return render_template('index.html')


@app.route('/about')
def about():
    return render_template('about.html')


# Страница "Все статьи на сайте"
@app.route('/posts')
def posts():
    articles = Article.query.order_by(Article.date.desc()).all()
    return render_template('posts.html', articles=articles)


# Получение полного текста статьи
@app.route('/posts/<int:id>')
def post_detail(id):
    article = Article.query.get(id)
    return render_template('post_detail.html', article=article)


# Удаление статьи
@app.route('/posts/<int:id>/del')
def post_delete(id):
    article = Article.query.get_or_404(id)

    try:
        db.session.delete(article)
        db.session.commit()
        return redirect('/posts')
    except:
        return "При удалении произошла ошибка!"


# Редактирование статьи
@app.route('/posts/<int:id>/update', methods=['POST', 'GET'])
def post_update(id):
    article = Article.query.get(id)
    if request.method == "POST":
        article.title = request.form['title']
        article.intro = request.form['intro']
        article.text = request.form['text']

        try:
            db.session.commit()
            return redirect('/posts')
        except:
            return "При редактировании статьи произошла ошибка!"
    else:
        return render_template('post_update.html', article=article)


# Добавление статьи
@app.route('/create-article', methods=['POST', 'GET'])
def create_article():
    if request.method == "POST":
        title = request.form['title']
        intro = request.form['intro']
        text = request.form['text']

        article = Article(title=title, intro=intro, text=text)

        try:
            db.session.add(article)
            db.session.commit()
            return redirect('/posts')
        except:
            return "При добавлении статьи произошла ошибка!"
    else:
        return render_template('create-article.html')


if __name__ == '__main__':
    app.run(debug=True)

