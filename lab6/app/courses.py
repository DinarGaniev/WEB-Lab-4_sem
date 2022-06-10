from unicodedata import category
from flask import Blueprint, render_template, request, flash, redirect, url_for
from app import db
from models import Course, Category, User, Review
from tools import CoursesFilter, ImageServer, ReviewsFilter
from flask_login import current_user

bp = Blueprint('courses', __name__, url_prefix='/courses')

PER_PAGE = 3

COMMENT_PAGE = 5

COMMENT_PER_PAGE = 10

COURSE_PARAMS = ['author_id', 'name', 'category_id', 'short_desc', 'full_desc']

COMMENT_PARAMS = ['rating', 'text', 'course_id', 'user_id']

def params():
    return { p: request.form.get(p) for p in COURSE_PARAMS}

def comment_params():
    return { p: request.form.get(p) for p in COMMENT_PARAMS }

def search_params():
    return {
        'name': request.args.get('name'),
        'category_ids': request.args.getlist('category_ids'),
    }

def search_params_comm(course_id):
    return {
        'name': request.args.get('name'),
        'category_ids': request.args.getlist('category_ids'),
        'course_id': course_id
    }

@bp.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    courses = CoursesFilter(**search_params()).perform()
    pagination = courses.paginate(page, PER_PAGE)
    courses = pagination.items
    categories = Category.query.all()
    return render_template('courses/index.html', courses=courses, categories=categories, pagination=pagination, search_params=search_params())

@bp.route('/new')
def new():
    categories = Category.query.all()
    users = User.query.all()
    return render_template('courses/new.html', categories=categories, users=users)

@bp.route('/create', methods=['POST'])
def create():
    
    f = request.files.get('background_img')
    if f and f.filename:
        img = ImageServer(f).save()

    course = Course(**params(), background_image_id=img.id )
    db.session.add(course)
    db.session.commit()

    flash(f'Курс {course.name} успешно добавлен')
    
    return redirect(url_for('courses.index'))

@bp.route('/<int:course_id>')
def show(course_id):
    courses = Course.query.get(course_id)
    reviews = Review.query.filter_by(course_id=course_id).limit(COMMENT_PAGE)
    user_review = None
    if current_user.is_authenticated is True:
        user_review = Review.query.filter_by(course_id=course_id, user_id=current_user.id).first()
    users = User.query.all()
    return render_template('courses/show.html', course=courses, review=reviews, users=users, user_review=user_review)


@bp.route('/<int:course_id>', methods=['POST'])
def send_comment(course_id):
    reviews = Review(**comment_params())
    courses = Course.query.filter_by(id=course_id).first()
    courses.rating_num += 1
    courses.rating_sum += int(reviews.rating)
    db.session.add(reviews)
    db.session.commit()
    flash('Комментарий был успешно добавлен!', 'success')

    return redirect(url_for('courses.show', course_id=courses.id))

@bp.route('/<int:course_id>/reviews')
def reviews(course_id):
    reviews = ReviewsFilter(course_id).perform_date_desc()
    courses = Course.query.filter_by(id=course_id).first()
    page = request.args.get('page', 1, type=int)
    pagination = reviews.paginate(page, COMMENT_PER_PAGE)
    reviews = pagination.items
    return render_template('courses/reviews.html', reviews=reviews, courses=courses, pagination=pagination, search_params=search_params_comm(course_id))


@bp.route('/<int:course_id>/reviews', methods=['POST'])
def reviews_sort(course_id):
    # reviews = ReviewsFilter(course_id).perform_date_desc()
    if request.form.get('sort') == 'new':
        reviews = ReviewsFilter(course_id).perform_date_desc()
    if request.form.get('sort') == 'old':
        reviews = ReviewsFilter(course_id).perform_date_asc()
    if request.form.get('sort') == 'good':
        reviews = ReviewsFilter(course_id).perform_rating_desc()
    if request.form.get('sort') == 'bad':
        reviews = ReviewsFilter(course_id).perform_rating_asc()
    req_form = request.form.get('sort')
    courses = Course.query.filter_by(id=course_id).first()
    page = request.args.get('page', 1, type=int)
    pagination = reviews.paginate(page, COMMENT_PER_PAGE)
    reviews = pagination.items
    return render_template('courses/reviews.html', reviews=reviews, courses=courses, req_form=req_form, pagination=pagination, search_params=search_params_comm(course_id))