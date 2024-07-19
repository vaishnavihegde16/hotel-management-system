import streamlit as st
import datetime
import DatabaseManager

from PIL import Image

# Define the discount percentage
DISCOUNT_PERCENTAGE = 10  # Example discount percentage

st.set_page_config(page_title="Hotel Booking", page_icon=":office:")

st.title('Welcome to Four Seasons Hotel')
st.write("The Four Seasons Hotel offers luxurious guest rooms, elegant dining options, a fitness center, "
         "spa, and indoor pool. Perfect choice for a memorable stay.")
st.write("---")


def get_room_images():
    return {
        1: 'Images/Room1.jpg',
        2: 'Images/Room2.jpg',
        3: 'Images/Room3.jpg',
        4: 'Images/Room4.jpg',
        5: 'Images/Room5.jpg'
    }


def display_room(roomtypeid):
    col1, col2 = st.columns([1, 1])
    row = DatabaseManager.getRoomType(roomtypeid)

    if row:
        
        
        
        
        
        with col1:
            image1 = Image.open('Images/Room1.jpg')
            st.image(image1)
            image2=Image.open('Images/Room2.jpg')
            st.image(image2)
            
                
        with col2:
            st.write(f'Room Number: {row[0]}')
            st.write(f'Description: {row[4]}')
            st.write(f'Number of Beds: {row[0]} || Air Conditioning: {row[2]}')
            st.write(f'Price: {row[3]}')
            st.write("---")

            st.write(f'Room Number: {row[1]}')
            st.write(f'Description: {row[4]}')
            st.write(f'Number of Beds: {row[1]} || Air Conditioning: {row[2]}')
            st.write(f'Price: {row[3]}')
            st.write("---")

def calculate_total_price(roomtypeid, checkin, checkout):
    total_price = DatabaseManager.selectRoom(roomtypeid, checkin, checkout)
    return total_price


def calculate_discounted_price(original_price):
    # Your discount calculation logic here
    discounted_price = original_price * (1 - DISCOUNT_PERCENTAGE / 100)
    return discounted_price


def main():
    st.header('Enter Details Below')
    col1, col2 = st.columns([1, 0.5])
    date = datetime.datetime.now().date()
    with col1:
        st.write('Enter Check-in and Check-out date')
    with col2:
        st.button(f"Today's Date 🗓️ {date}")

    col5, col6 = st.columns(2)
    with col5:
        checkin = st.date_input('Enter Check-in Date🗓️')
    with col6:
        checkout = st.date_input('Enter Check-out Date🗓️')

    cname = st.text_input('Enter Your Full Name')
    cage = int(st.number_input('Enter Your Age', step=1))
    aadhar = st.text_input('Enter your SSN/Aadhaar')
    phone = st.text_input('Enter your phone number')
    caddress = st.text_area('Enter Your Address')

    st.write("---")
    st.header('Select Room')

    for roomtypeid in range(1, 6):
        display_room(roomtypeid)

    roomtypeid = st.number_input('Select Room Number', step=1)
    flag = 0

    if st.button('Submit'):
        if checkin > checkout:
            st.error('Check-out cannot be before check-in')
            flag = 1
        try:
            int(aadhar.replace(' ', ''))
        except ValueError:
            st.error('(SSN/Aadhaar) cannot have letters')
            flag = 1
        else:
            aadhar = int(aadhar.replace(' ', ''))
        if cage < 18:
            st.error('You need to be an adult to book a hotel room')
            flag = 1
        if len(phone) != 10:
            st.error('Phone Number must be 10 digits')
            flag = 1
        try:
            int(phone)
        except ValueError:
            st.error('Phone Number cannot have letters')
            flag = 1
        else:
            phone = int(phone)
        if flag == 0:
            st.success('Details Saved')

        if roomtypeid < 1 or roomtypeid > 5:
            st.error('Room Does Not Exist')
            flag = 1
        try:
            int(roomtypeid)
        except ValueError:
            st.error('Room Number cannot have letters')
            flag = 1
        else:
            roomtypeid = int(roomtypeid)
        if flag == 0:
            total_price = calculate_total_price(roomtypeid, checkin, checkout)
            discounted_price = calculate_discounted_price(total_price)
            cid = DatabaseManager.addCustDetails(aadhar, cname, cage, phone, caddress, discounted_price, checkin, checkout)
            end(cid, checkin, checkout,total_price, discounted_price)


def end(cid, checkin, checkout, total_price,discounted_price):
    st.write("---")
    row = DatabaseManager.getCustDetails(cid)
    

    st.success('Booking Confirmed')
    st.write(f'Customer ID: {cid}')
    st.write(f'Customer Name: {row[2]}')
    st.write(f'Customer Aadhaar: {row[1]}')
    st.write(f'Check In: {checkin}')
    st.write(f'Check Out: {checkout}')
    st.write(f'Customer Phone Number: {row[4]}')
    st.write(f'Original Room Amount: {total_price}')
    st.write(f'Discounted Room Amount: {discounted_price}')
    st.info('Bill will be due after your Stay')



if __name__ == "__main__":
    main()
