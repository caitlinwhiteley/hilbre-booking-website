'use client'

import { useEffect, useState } from 'react'
import api from './api'
import Input from './components/input'

type TBookings = {
  date: string
  numberOfDays: number
  numberOfPeople: number
  price: number
  hasPaid: boolean
  otherAttendees: string | undefined
  bookingStatus: string
  bookingComments: string | undefined
  userId: number
}

export default function Home() {
  const defaultFormData = {
    date: '',
    numberOfDays: 7,
    numberOfPeople: 0,
    price: 0,
    hasPaid: false,
    otherAttendees: '',
    bookingStatus: '', // think this is set as a default in the BE?
    bookingComments: '',
    userId: 1, // get from context when person logged in
  }

  const [bookings, setBookings] = useState<TBookings[]>()
  const [formData, setFormData] =
    useState<Omit<TBookings, 'id'>>(defaultFormData)

  const fetchTransactions = async () => {
    try {
      const response = await api.get('/bookings/')
      console.log('Full response:', response)
      if (response.data) {
        setBookings(response.data)
      } else {
        console.error('No response data received', response)
      }
    } catch (error) {
      console.error('Error fetching bookings:', error)
    }
  }

  useEffect(() => {
    fetchTransactions()
  }, [])

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const value =
      e.target.type === 'number' ? Number(e.target.value) : e.target.value
    setFormData({ ...formData, [e.target.name]: value })
  }

  const handleFormSubmit = async (event: React.FormEvent) => {
    event.preventDefault() // don't submit form - we want to handle the action of submitting the form
    console.log('Sending data:', formData)
    await api.post('/bookings/', formData)
    fetchTransactions()
    setFormData(defaultFormData)
  }

  const inputData = [
    {
      name: 'date',
      type: 'date',
      value: formData.date,
      label: 'Start date',
    },
    {
      name: 'numberOfDays',
      type: 'number',
      value: formData.numberOfDays,
      label: 'Number of days',
    },
    {
      name: 'numberOfPeople',
      type: 'number',
      value: formData.numberOfPeople,
      label: 'Number of people',
    },
    {
      name: 'price',
      type: 'number',
      value: formData.price,
      label: 'Price',
    },
    {
      name: 'otherAttendees',
      type: 'text',
      value: formData.otherAttendees,
      label: 'Other attendees',
    },
    {
      name: 'bookingComments',
      type: 'text',
      value: formData.bookingComments,
      label: 'Booking comments',
    },
  ]

  console.log('bookings = ', bookings)

  return (
    <div className="grid grid-rows-[20px_1fr_20px] items-center justify-items-center min-h-screen p-8 pb-20 gap-16 sm:p-20 font-[family-name:var(--font-geist-sans)]">
      <main className="flex flex-col gap-8 row-start-2 items-center sm:items-start">
        <h1>Test Form!</h1>

        <div>
          <form onSubmit={handleFormSubmit}>
            {inputData.map(({ value, label, name, type }) => (
              <Input
                onChange={handleInputChange}
                value={value}
                label={label}
                name={name}
                type={type}
                key={name}
              />
            ))}

            <button
              className="mt-6 bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
              type="submit"
            >
              Submit
            </button>
          </form>
        </div>

        <table className="table-auto">
          <thead>
            <tr>
              <td>date</td>
              <td>numberOfPeople</td>
              <td>numberOfDays</td>
              <td>price</td>
              <td>hasPaid</td>
              <td>otherAttendees</td>
              <td>bookingStatus</td>
              <td>bookingComments</td>
            </tr>
          </thead>
          <tbody>
            {bookings?.map(
              ({
                date,
                numberOfDays,
                numberOfPeople,
                price,
                hasPaid,
                otherAttendees,
                bookingStatus,
                bookingComments,
                // userId,
              }) => (
                <tr key={Math.random()}>
                  <td>{date}</td>
                  <td>{numberOfPeople}</td>
                  <td>{numberOfDays}</td>
                  <td>{price}</td>
                  <td>{hasPaid}</td>
                  <td>{otherAttendees}</td>
                  <td>{bookingStatus}</td>
                  <td>{bookingComments}</td>
                </tr>
              )
            )}
          </tbody>
        </table>
      </main>
      <footer className="row-start-3 flex gap-6 flex-wrap items-center justify-center"></footer>
    </div>
  )
}
