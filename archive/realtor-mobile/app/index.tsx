import { useEffect, useState } from 'react'
import { View, Text, FlatList, ActivityIndicator } from 'react-native'
import { api } from '../shared/services/api'
import { Property } from '../shared/types'
import PropertyCard from '../src/modules/properties/PropertyCard'

export default function PropertiesScreen() {
  const [properties, setProperties] = useState<Property[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    api.get('/properties/')
      .then(res => {
        setProperties(res.data.results || res.data)
        setLoading(false)
      })
      .catch(() => setLoading(false))
  }, [])

  if (loading) {
    return (
      <View className="flex-1 justify-center items-center">
        <ActivityIndicator size="large" color="#10b981" />
      </View>
    )
  }

  return (
    <View className="flex-1 bg-gray-50">
      <FlatList
        data={properties}
        keyExtractor={item => item.id.toString()}
        renderItem={({ item }) => <PropertyCard property={item} />}
        contentContainerClassName="p-4"
      />
    </View>
  )
}
