package es.gameshelf.domain.interfaces.service;

import es.gameshelf.domain.Role;

import java.util.List;
/**
 * @author Nabil L. A. @nalleon
 */
public interface IRoleService {
    Role add(String name);
    Role findById(Integer id);
    Role findByName (String username);
    List<Role> findAll();
    boolean delete(Integer id);
    Role update(int id, String name);
}

