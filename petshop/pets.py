import datetime

from flask import Blueprint
@@ -18,25 +19,36 @@ def format_date(d):

@bp.route("/search/<field>/<value>")
def search(field, value):
    # TBD
    return ""
    conn = db.get_db()
    cursor = conn.cursor()
    oby = request.args.get("order_by", "id")
    order = request.args.get("order", "asc")
    cursor.execute("select tag.id from tag where tag.name = ?",[value])
    tag_no = cursor.fetchall()[0][0]
    print(tag_no, " ", type(tag_no))
    if order == "asc":
        cursor.execute("select pet.id, pet.name, pet.bought, pet.sold, s.name from pet , animal s where pet.species = s.id and pet.id in (select tags_pets.pet from tags_pets where tags_pets.tag = ?) order by pet.id",[tag_no])
    else:
        cursor.execute("select pet.id, pet.name, pet.bought, pet.sold, s.name from pet , animal s where pet.species = s.id and pet.id in (select tags_pets.pet from tags_pets where tags_pets.tag = ?) order by pet.id desc",[tag_no])
    pets = cursor.fetchall()
    return render_template('index.html', pets = pets, order="desc" if order=="asc" else "asc")

@bp.route("/")
def dashboard():
    conn = db.get_db()
    cursor = conn.cursor()
    oby = request.args.get("order_by", "id") # TODO. This is currently not used. 
    oby = request.args.get("order_by", "id") # TODO. This is currently not used.
    order = request.args.get("order", "asc")
    if order == "asc":
        cursor.execute(f"select p.id, p.name, p.bought, p.sold, s.name from pet p, animal s where p.species = s.id order by p.id")
        cursor.execute(f"select p.id, p.name, p.bought, p.sold, s.name from pet p, animal s where p.species = s.id order by p.{oby}")
    else:
        cursor.execute(f"select p.id, p.name, p.bought, p.sold, s.name from pet p, animal s where p.species = s.id order by p.id desc")
        cursor.execute(f"select p.id, p.name, p.bought, p.sold, s.name from pet p, animal s where p.species = s.id order by p.{oby} desc")
    pets = cursor.fetchall()
    return render_template('index.html', pets = pets, order="desc" if order=="asc" else "asc")


@bp.route("/<pid>")
def pet_info(pid): 
def pet_info(pid):
    conn = db.get_db()
    cursor = conn.cursor()
    cursor.execute("select p.name, p.bought, p.sold, p.description, s.name from pet p, animal s where p.species = s.id and p.id = ?", [pid])
@@ -74,10 +86,20 @@ def edit(pid):
    elif request.method == "POST":
        description = request.form.get('description')
        sold = request.form.get("sold")
        # TODO Handle sold
        return redirect(url_for("pets.pet_info", pid=pid), 302)



        cursor.execute("update pet set description = ? where pet.id = ?",[description, pid])
        print(sold)
        if(sold):
            d1 = datetime.datetime.now()
            curr_date = d1.strftime('%Y-%m-%d')
            print(curr_date)
            print(type(curr_date))
            cursor.execute("update pet set sold = ? where pet.id = ?",[curr_date, pid])

        cursor.close()
        conn.commit()
        db.close_db()


        # TODO Handle sold
        return redirect(url_for("pets.pet_info", pid=pid), 302)
    



