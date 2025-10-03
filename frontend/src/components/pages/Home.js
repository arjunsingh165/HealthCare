import React from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../../contexts/AuthContext';
import { 
  HeartIcon, 
  UserGroupIcon, 
  ClockIcon,
  ShieldCheckIcon,
  StarIcon,
  PhoneIcon,
  MapPinIcon,
  EnvelopeIcon
} from '@heroicons/react/24/outline';

const Home = () => {
  const { isAuthenticated, user } = useAuth();

  const features = [
    {
      icon: UserGroupIcon,
      title: 'Expert Doctors',
      description: 'Access to qualified healthcare professionals across various specializations.'
    },
    {
      icon: ClockIcon,
      title: '24/7 Support',
      description: 'Round-the-clock healthcare support and emergency consultations.'
    },
    {
      icon: ShieldCheckIcon,
      title: 'Secure & Private',
      description: 'Your health data is protected with enterprise-grade security.'
    },
    {
      icon: HeartIcon,
      title: 'Personalized Care',
      description: 'Tailored healthcare solutions based on your individual needs.'
    }
  ];

  const specializations = [
    'Cardiology', 'Dermatology', 'Endocrinology', 'Gastroenterology',
    'General Medicine', 'Gynecology', 'Neurology', 'Oncology',
    'Orthopedics', 'Pediatrics', 'Psychiatry', 'Pulmonology'
  ];

  const testimonials = [
    {
      name: 'Sarah Johnson',
      role: 'Patient',
      content: 'HealthCare Pro made it so easy to find and book appointments with top doctors. The platform is user-friendly and the doctors are excellent.',
      rating: 5
    },
    {
      name: 'Dr. Michael Chen',
      role: 'Cardiologist',
      content: 'As a healthcare provider, I appreciate how this platform streamlines patient management and communication. It\'s a game-changer.',
      rating: 5
    },
    {
      name: 'Emily Rodriguez',
      role: 'Patient',
      content: 'The chat feature is fantastic for follow-ups. I can easily communicate with my doctor without needing to schedule another appointment.',
      rating: 5
    }
  ];

  return (
    <div className="min-h-screen">
      {/* Hero Section */}
      <section className="health-hero py-20 px-4">
        <div className="max-w-7xl mx-auto text-center text-white">
          <h1 className="text-5xl md:text-6xl font-bold mb-6">
            Your Health, <span className="text-health-secondary">Our Priority</span>
          </h1>
          <p className="text-xl md:text-2xl mb-8 opacity-90 max-w-3xl mx-auto">
            Connect with qualified healthcare professionals, book appointments, and manage your health journey with ease.
          </p>
          <div className="flex flex-col sm:flex-row justify-center items-center space-y-4 sm:space-y-0 sm:space-x-4">
            {!isAuthenticated ? (
              <>
                <Link to="/register" className="bg-white text-health-primary px-8 py-4 rounded-lg font-semibold text-lg hover:bg-gray-100 transition-colors">
                  Get Started Today
                </Link>
                <Link to="/doctors" className="border-2 border-white text-white px-8 py-4 rounded-lg font-semibold text-lg hover:bg-white hover:text-health-primary transition-colors">
                  Find Doctors
                </Link>
              </>
            ) : (
              <Link to="/dashboard" className="bg-white text-health-primary px-8 py-4 rounded-lg font-semibold text-lg hover:bg-gray-100 transition-colors">
                Go to Dashboard
              </Link>
            )}
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-20 px-4 bg-white">
        <div className="max-w-7xl mx-auto">
          <div className="text-center mb-16">
            <h2 className="text-4xl font-bold text-health-dark mb-4">
              Why Choose HealthCare Pro?
            </h2>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto">
              We're committed to providing you with the best healthcare experience through innovative technology and expert care.
            </p>
          </div>
          
          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8">
            {features.map((feature, index) => (
              <div key={index} className="health-card text-center">
                <feature.icon className="h-12 w-12 text-health-primary mx-auto mb-4" />
                <h3 className="text-xl font-semibold text-health-dark mb-3">
                  {feature.title}
                </h3>
                <p className="text-gray-600">
                  {feature.description}
                </p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Specializations Section */}
      <section className="py-20 px-4 bg-health-light">
        <div className="max-w-7xl mx-auto">
          <div className="text-center mb-16">
            <h2 className="text-4xl font-bold text-health-dark mb-4">
              Medical Specializations
            </h2>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto">
              Find expert doctors across a wide range of medical specializations.
            </p>
          </div>
          
          <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
            {specializations.map((specialization, index) => (
              <Link
                key={index}
                to={`/doctors?specialization=${specialization.toLowerCase()}`}
                className="bg-white p-4 rounded-lg text-center hover:shadow-lg transition-all duration-300 hover:transform hover:-translate-y-1"
              >
                <span className="text-health-dark font-medium">{specialization}</span>
              </Link>
            ))}
          </div>
        </div>
      </section>

      {/* Testimonials Section */}
      <section className="py-20 px-4 bg-white">
        <div className="max-w-7xl mx-auto">
          <div className="text-center mb-16">
            <h2 className="text-4xl font-bold text-health-dark mb-4">
              What Our Users Say
            </h2>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto">
              Don't just take our word for it. Here's what patients and doctors have to say about HealthCare Pro.
            </p>
          </div>
          
          <div className="grid md:grid-cols-3 gap-8">
            {testimonials.map((testimonial, index) => (
              <div key={index} className="health-card">
                <div className="flex items-center mb-4">
                  {[...Array(testimonial.rating)].map((_, i) => (
                    <StarIcon key={i} className="h-5 w-5 text-yellow-400 fill-current" />
                  ))}
                </div>
                <p className="text-gray-600 mb-4 italic">
                  \"{testimonial.content}\"
                </p>
                <div>
                  <p className="font-semibold text-health-dark">{testimonial.name}</p>
                  <p className="text-sm text-gray-500">{testimonial.role}</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Stats Section */}
      <section className="py-20 px-4 health-gradient text-white">
        <div className="max-w-7xl mx-auto">
          <div className="grid md:grid-cols-4 gap-8 text-center">
            <div>
              <h3 className="text-4xl font-bold mb-2">500+</h3>
              <p className="text-lg opacity-90">Qualified Doctors</p>
            </div>
            <div>
              <h3 className="text-4xl font-bold mb-2">10K+</h3>
              <p className="text-lg opacity-90">Happy Patients</p>
            </div>
            <div>
              <h3 className="text-4xl font-bold mb-2">50K+</h3>
              <p className="text-lg opacity-90">Appointments Booked</p>
            </div>
            <div>
              <h3 className="text-4xl font-bold mb-2">24/7</h3>
              <p className="text-lg opacity-90">Support Available</p>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 px-4 bg-health-light">
        <div className="max-w-4xl mx-auto text-center">
          <h2 className="text-4xl font-bold text-health-dark mb-4">
            Ready to Take Control of Your Health?
          </h2>
          <p className="text-xl text-gray-600 mb-8">
            Join thousands of satisfied patients and healthcare providers on HealthCare Pro.
          </p>
          {!isAuthenticated && (
            <div className="flex flex-col sm:flex-row justify-center items-center space-y-4 sm:space-y-0 sm:space-x-4">
              <Link to="/register" className="health-button text-lg px-8 py-4">
                Sign Up Now
              </Link>
              <Link to="/doctors" className="health-button-secondary text-lg px-8 py-4">
                Browse Doctors
              </Link>
            </div>
          )}
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-health-dark text-white py-12 px-4">
        <div className="max-w-7xl mx-auto">
          <div className="grid md:grid-cols-4 gap-8">
            <div>
              <div className="flex items-center space-x-2 mb-4">
                <HeartIcon className="h-8 w-8 text-health-secondary" />
                <span className="text-xl font-bold">HealthCare Pro</span>
              </div>
              <p className="text-gray-300">
                Your trusted partner in healthcare, connecting patients with the best medical professionals.
              </p>
            </div>
            
            <div>
              <h3 className="text-lg font-semibold mb-4">Quick Links</h3>
              <ul className="space-y-2">
                <li><Link to="/doctors" className="text-gray-300 hover:text-white transition-colors">Find Doctors</Link></li>
                <li><Link to="/register" className="text-gray-300 hover:text-white transition-colors">Sign Up</Link></li>
                <li><Link to="/login" className="text-gray-300 hover:text-white transition-colors">Login</Link></li>
              </ul>
            </div>
            
            <div>
              <h3 className="text-lg font-semibold mb-4">Support</h3>
              <ul className="space-y-2">
                <li><a href="#" className="text-gray-300 hover:text-white transition-colors">Help Center</a></li>
                <li><a href="#" className="text-gray-300 hover:text-white transition-colors">Privacy Policy</a></li>
                <li><a href="#" className="text-gray-300 hover:text-white transition-colors">Terms of Service</a></li>
              </ul>
            </div>
            
            <div>
              <h3 className="text-lg font-semibold mb-4">Contact Us</h3>
              <div className="space-y-2">
                <div className="flex items-center space-x-2">
                  <PhoneIcon className="h-5 w-5 text-health-secondary" />
                  <span className="text-gray-300">+1 (555) 123-4567</span>
                </div>
                <div className="flex items-center space-x-2">
                  <EnvelopeIcon className="h-5 w-5 text-health-secondary" />
                  <span className="text-gray-300">support@healthcarepro.com</span>
                </div>
                <div className="flex items-center space-x-2">
                  <MapPinIcon className="h-5 w-5 text-health-secondary" />
                  <span className="text-gray-300">123 Health St, Medical City</span>
                </div>
              </div>
            </div>
          </div>
          
          <div className="border-t border-gray-700 mt-8 pt-8 text-center">
            <p className="text-gray-300">
              © 2025 HealthCare Pro. All rights reserved.
            </p>
          </div>
        </div>
      </footer>
    </div>
  );
};

export default Home;