export interface Property {
  id: number
  title: string
  price: number
  price_type: "sale" | "rent"
  location: string
  image: string
  description: string
  bedrooms: number
  bathrooms: number
}

export interface User {
  id: number
  username: string
  email: string
}
