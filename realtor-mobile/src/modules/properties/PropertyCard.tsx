import { View, Text, Image, TouchableOpacity } from 'react-native'
import { useRouter } from 'expo-router'
import { Property } from '../../../shared/types'
import { formatPriceINR } from '../../../shared/utils/formatPriceINR'

export default function PropertyCard({ property }: { property: Property }) {
  const router = useRouter()

  return (
    <TouchableOpacity onPress={() => router.push(`/property/${property.id}`)}>
      <View className="bg-white rounded-lg shadow-md p-4 mb-4">
        <Image
          source={{ uri: property.image || 'https://via.placeholder.com/400' }}
          className="w-full h-48 rounded-lg"
          resizeMode="cover"
        />
        <Text className="font-semibold text-lg mt-2">{property.title}</Text>
        <Text className="text-gray-500 text-sm">{property.location}</Text>
        <View className="flex-row justify-between items-center mt-3">
          <Text className="text-green-600 font-bold text-lg">
            {formatPriceINR(property.price, property.price_type)}
          </Text>
          <View className="flex-row gap-3">
            <Text className="text-gray-600">🛏️ {property.bedrooms}</Text>
            <Text className="text-gray-600">🚿 {property.bathrooms}</Text>
          </View>
        </View>
      </View>
    </TouchableOpacity>
  )
}
