import React from 'react'

interface IInputProps {
  onChange: (e: React.ChangeEvent<HTMLInputElement>) => void
  value: string | number | readonly string[] | undefined
  label: string
  name: string
  type: React.HTMLInputTypeAttribute
}

const Input = ({
  onChange,
  value,
  label,
  name,
  type,
  ...props
}: IInputProps) => {
  return (
    <div>
      <label
        htmlFor={name}
        className="block mb-2 mt-6 text-sm font-medium text-gray-900 dark:text-white"
      >
        {label}
      </label>
      <input
        id={name}
        className="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
        {...{ type, name, onChange, value }}
        {...props}
      />
    </div>
  )
}

export default Input
