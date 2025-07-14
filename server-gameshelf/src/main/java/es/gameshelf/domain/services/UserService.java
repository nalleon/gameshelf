package es.gameshelf.domain.services;

import es.gameshelf.domain.Role;
import es.gameshelf.domain.User;
import es.gameshelf.domain.WishListItem;
import es.gameshelf.domain.interfaces.repository.IRoleRepository;
import es.gameshelf.domain.interfaces.repository.IUserRepository;
import es.gameshelf.domain.interfaces.service.IUserService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.Map;

/**
 * @author Nabil L. A. @nalleon
 */
@Service
public class UserService implements IUserService {
    /**
     * Properties
     */
    IUserRepository repository;

    /**
     * Setter for the autowired service
     * @param repository of the service
     */
    @Autowired
    public void setRepository(IUserRepository repository) {
        this.repository = repository;
    }

    @Override
    public User add(String username, String email, String password) {
        User item = new User(username, email, password);
        return repository.save(item);
    }

    @Override
    public List<User> findAll() {
        return repository.findAll();
    }

    @Override
    public List<WishListItem> findAllByRole(Role role) {
        return repository.findAllByRole(role);
    }

    @Override
    public Map<Role, Integer> countAllGroupedByRole() {
        return repository.countAllGroupedByRole();
    }

    @Override
    public User findById(Integer id) {
        return repository.findById(id);
    }

    @Override
    public User findByUsername(String username) {
        return repository.findByUsername(username);
    }

    @Override
    public User findByEmail(String email) {
        return repository.findByEmail(email);
    }

    @Override
    public boolean delete(Integer id) {
        return repository.delete(id);
    }

    @Override
    public User update(Integer id, String username, String email, String password, String profilePictureRole, Role role) {
        User item = new User(id, username, email, password, profilePictureRole, role);
        return repository.update(item);
    }

    @Override
    public User updatePassword(Integer id, String password) {

        User item = new User(id);
        item.setPassword(password);

        return repository.updatePassword(item);
    }

    @Override
    public User updateUsername(Integer id, String username) {

        User item = new User(id);
        item.setUsername(username);

        return repository.updateUsername(item);    }

    @Override
    public User updateEmail(Integer id, String email) {
        User item = new User(id);
        item.setEmail(email);

        return repository.updateEmail(item);
    }

    @Override
    public User updatePicture(Integer id, String profilePicture) {
        User item = new User(id);
        item.setProfilePicture(profilePicture);

        return repository.updatePicture(item);     }

    @Override
    public User updateRole(Integer id, Role role) {
        User item = new User(id);
        item.setRole(role);

        return repository.updateRole(item);
    }

    @Override
    public User verify(Integer id) {
        return repository.verify(new User(id));
    }
}
